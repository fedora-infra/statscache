import socket
hostname = socket.gethostname().split('.')[0]


config = {
    # Consumer stuff
    "statscache.consumer.enabled": True,
    "statscache.sqlalchemy.uri": "sqlite:////var/tmp/statscache-dev-db.sqlite",
}
