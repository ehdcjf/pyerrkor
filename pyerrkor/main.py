from pyerrkor import registry
from pyerrkor.handlers import *


def install(exc_type, exc_value):
    handler = registry.get_handler()
