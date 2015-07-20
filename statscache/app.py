import flask
import fedmsg.config
import statscache.plugins
import statscache.utils
import statscache.frequency
import json

app = flask.Flask(__name__)

config = fedmsg.config.load_config()
plugins = {} # mapping of identifiers to plugin instances

uri = config['statscache.sqlalchemy.uri']
session = statscache.plugins.init_model(uri)


def jsonp(body, status):
    """ Helper function to send either a JSON or JSON-P response """
    mimetype = 'application/json'
    callback = flask.request.args.get('callback')
    if callback:
        body = '{}({})'.format(callback, body)
        mimetype = 'application/javascript'
    return flask.Response(
        response=body,
        status=status,
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


def respond(model, rows, status):
    """
    Helper function to generate a response in the appropriate content-type
    """
    mimetype = get_mimetype()
    if mimetype.endswith('json') or mimetype.endswith('javascript'):
        return jsonp(model.to_json(rows), status)
    elif mimetype.endswith('csv'):
        return flask.Response(
            response=model.to_csv(rows),
            status=status,
            mimetype=mimetype
        )
#    elif mimetype.endswith('html'):
#        return render_template('view.html', data=model.to_json(rows)), status
    else:
        flask.abort(406)


@app.route('/')
def index():
    """ Generate a JSON-P response with an index of plugins (as an array) """
    mimetype = get_mimetype()
    if not mimetype.endswith('json') and not mimetype.endswith('javascript'):
        flask.abort(406)
    return jsonp(json.dumps(plugins.keys()), 200)


@app.route('/<name>')
def main(name):
    """ Generate a JSON-P response with the content of the plugin's model """
    plugin = plugins.get(name)
    if not hasattr(plugin, 'model'):
        flask.abort(404)
    return respond(plugin.model, session.query(plugin.model).all(), 200)


@app.route('/<name>/layout')
def plugin_layout(name):
    """ Generate a JSON-P response with the content of the plugin's layout """
    plugin = plugins.get(name)
    mimetype = get_mimetype()
    if not mimetype.endswith('json') and not mimetype.endswith('javascript'):
        flask.abort(406)
    if not hasattr(plugin, 'layout'):
        flask.abort(404)
    return jsonp(json.dumps(plugin.layout), 200)


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
    frequencies = { None: None } # mapping of intervals to reusable Frequency instances
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
