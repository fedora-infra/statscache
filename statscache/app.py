import flask
import fedmsg.config
import statscache.plugins
import statscache.utils

app = flask.Flask(__name__)

config = fedmsg.config.load_config()

uri = config['statscache.sqlalchemy.uri']
session = statscache.plugins.init_model(uri)

@app.route('/<name>')
def main(name):
    model = statscache.utils.get_model(name, frequency=5, config=config)
    results = session.query(model).all()
    return model.to_csv(results)


if __name__ == '__main__':
    app.run(
        debug=True,
    )

