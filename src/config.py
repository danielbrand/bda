import os

__author__ = "Daniel Brand"

DEBUG = True

ADMINS = frozenset([
    os.environ.get("EMAIL")
])
