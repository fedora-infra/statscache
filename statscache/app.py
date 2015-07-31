import flask
import fedmsg.config
import statscache.plugins
import statscache.utils
import statscache.frequency
import json
import datetime

app = flask.Flask(__name__)

config = fedmsg.config.load_config()
plugins = {} # mapping of identifiers to plugin instances

uri = config['statscache.sqlalchemy.uri']
session = statscache.plugins.init_model(uri)


def jsonp(body):
    """ Helper function to send either a JSON or JSON-P response """
    mimetype = 'application/json'
    callback = flask.request.args.get('callback')
    if callback:
        body = '{}({})'.format(callback, body)
        mimetype = 'application/javascript'
    return flask.Response(
        response=body,
        status=200,
        mimetype=mimetype
    )


def get_mimetype():
    """ Get the most acceptable supported mimetype """
    return flask.request.accept_mimetypes.best_match([
        'application/json',
        'text/json',
        'application/javascript',
        'text/javascript',
        'application/csv',
        'text/csv',
#        'text/html', # currently, no HTML renderers have been implemented
    ]) or ""


@app.route('/api/')
def plugin_index():
    """ Get an index of the available plugins (as an array) """
    mimetype = get_mimetype()
    if not mimetype.endswith('json') and not mimetype.endswith('javascript'):
        flask.abort(406)
    return jsonp(json.dumps(plugins.keys()))


@app.route('/api/<name>')
def plugin_model(name):
    """ Get the contents of the plugin's model

    Arguments (from query string):
        order: ascend ('asc') or descend ('desc') results by timestamp
        start: exclude results older than the given UTC timestamp
        stop: exclude results newer than the given UTC timestamp
    """
    plugin = plugins.get(name)
    if not hasattr(plugin, 'model'):
        return '"No such model for \'{}\'"'.format(name), 404
    model = plugin.model
    query = session.query(model)
    # order the query
    if flask.request.args.get('order') == 'asc':
        query = query.order_by(model.timestamp.asc())
    else:
        query = query.order_by(model.timestamp.desc())
    # filter the query by the desired time window
    start = flask.request.args.get('start')
    if start is not None:
        query = query.filter(
            model.timestamp >= datetime.datetime.fromtimestamp(int(start))
        )
    stop = flask.request.args.get('stop')
    if stop is not None:
        query = query.filter(
            model.timestamp <= datetime.datetime.fromtimestamp(int(stop))
        )

    mimetype = get_mimetype()
    if mimetype.endswith('json') or mimetype.endswith('javascript'):
        return jsonp(model.to_json(query.all()))
    elif mimetype.endswith('csv'):
        return flask.Response(
            response=model.to_csv(query.all()),
            status=200,
            mimetype=mimetype
        )
#    elif mimetype.endswith('html'):
#        return flask.render_template('view.html', data=model.to_json(rows))
    else:
        flask.abort(406)


@app.route('/api/<name>/layout')
def plugin_layout(name):
    """ Get the layout of the plugin """
    plugin = plugins.get(name)
    mimetype = get_mimetype()
    if not mimetype.endswith('json') and not mimetype.endswith('javascript'):
        flask.abort(406)
    if not hasattr(plugin, 'layout'):
        flask.abort(404)
    return jsonp(json.dumps(plugin.layout))


@app.errorhandler(404)
def resource_not_found(error):
    name = (flask.request.view_args or {}).get('name')
    msg = "No such resource"
    if name is not None:
        msg += " for {}".format(name)
    return flask.Response(
        response=msg,
        mimetype='text/plain',
        status=404
    )


@app.errorhandler(406)
def unacceptable_content(error):
    return flask.Response(
        response="Content-type(s) not available",
        mimetype='text/plain',
        status=406
    )


if __name__ == '__main__':
    # initialize plugins
    frequencies = { None: None } # mapping of intervals to Frequency instances
    for plugin_class in statscache.utils.plugin_classes:
        if plugin_class.interval not in frequencies:
            frequencies[plugin_class.interval] = \
                statscache.frequency.Frequency(plugin_class.interval)
        plugin = plugin_class(frequencies[plugin_class.interval], config)
        plugins[plugin.ident] = plugin
    # ...and fire up the web app
    app.run(
        debug=True,
    )
