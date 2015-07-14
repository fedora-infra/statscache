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


@app.route('/<name>')
def main(name):
    """ Generate a JSON-P response with the content of the plugin's model """
    callback = flask.request.args.get('callback')
    model = None
    try:
        model = plugins.get(name).model
    except AttributeError:
        raise KeyError("No such model for %r" % name)
    results = session.query(model).all()
    body = model.to_json(results)
    if callback:
        body = '{}({})'.format(callback, body)
    status = 200
    mimetype = 'application/javascript'
    return flask.Response(
        response=body,
        status=status,
        mimetype=mimetype
    )


@app.route('/<name>/layout')
def plugin_layout(name):
    """ Generate a JSON-P response with the content of the plugin's layout """
    plugin = plugins.get(name)
    body = ''
    status = 404
    callback = flask.request.args.get('callback')
    mimetype = 'application/javascript'
    if plugin and hasattr(plugin, 'layout'):
        body = json.dumps(plugin.layout)
        status = 200
    if callback:
        body = '{}({})'.format(callback, body)
    return flask.Response(
        response=body,
        status=status,
        mimetype=mimetype
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
