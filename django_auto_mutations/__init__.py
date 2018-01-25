import os

from .auto_mutation import AutoMutation

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as version:
    VERSION = version.read()

__all__ = [
    'VERSION',
    'AutoMutation'
]
