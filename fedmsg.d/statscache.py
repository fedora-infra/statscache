import socket
hostname = socket.gethostname().split('.')[0]


config = {
    # Consumer stuff
    "statscache.consumer.enabled": True,
    "statscache.sqlalchemy.uri": "sqlite:////var/tmp/statscache-dev-db.sqlite",

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
