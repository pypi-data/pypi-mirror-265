
import os
from .agentfactory import initialize_agent, get_agent
from .custom_api import *
name = "apminsight"

version = "1.4.0"

installed_path = os.path.dirname(__file__)

__all__ =[
    'name',
    'version',
    'installed_path',
    'get_agent',
    'initialize_agent',
]
