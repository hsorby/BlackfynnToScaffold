import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    PENNSIEVE_API_HOST = os.environ.get("PENNSIEVE_API_HOST")
    PENNSIEVE_API_SECRET = os.environ.get("PENNSIEVE_API_SECRET", "local-secret")
    PENNSIEVE_API_TOKEN = os.environ.get("PENNSIEVE_API_TOKEN", "local-token")

