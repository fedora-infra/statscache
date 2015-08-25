import socket
import datetime
hostname = socket.gethostname().split('.')[0]


config = {
    "statscache.datagrepper.workers": 8,
    # Consumer stuff
    "statscache.consumer.enabled": True,
    "statscache.sqlalchemy.uri": "sqlite:////var/tmp/statscache-dev-db.sqlite",
    # stats models will go back at least this far (current value arbitrary)
    "statscache.consumer.epoch": datetime.datetime(year=2015, month=8, day=8),
    # stats models are updated at this frequency
    "statscache.producer.frequency": datetime.timedelta(seconds=1),
    # Turn on logging for statscache
    "logging": dict(
        loggers=dict(
            statscache={
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console"],
            },
            statscache_plugins={
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console"],
            },
        ),
    ),
}
