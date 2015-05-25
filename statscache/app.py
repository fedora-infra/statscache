import flask
import fedmsg.config
import statscache.plugins
import statscache.utils
import json

app = flask.Flask(__name__)

config = fedmsg.config.load_config()

uri = config['statscache.sqlalchemy.uri']
session = statscache.plugins.init_model(uri)

@app.route('/<name>')
def main(name):
    callback = flask.request.args.get('callback')
    #FIXME: Need to find a better way to pass 'frequency'
    model = statscache.utils.get_model(name, config=config)
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
    #FIXME: Need to find a better way to pass 'frequency'
    plugin = statscache.utils.get_plugin(name, config=config)
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
    app.run(
        debug=True,
    )

