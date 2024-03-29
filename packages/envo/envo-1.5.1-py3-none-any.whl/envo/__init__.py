# flake8: noqa E402, F401

import warnings
import sys

warnings.warn = lambda *args, **kwargs: None
warnings._showwarnmsg = lambda x: None

# warnings.simplefilter("ignore")

from rich.console import Console

console = Console()
console._force_terminal = True

from envo import e2e
from envo.logs import logger
from envo.devops import *
from envo.env import *
from envo.plugins import *
from envo.utils import *
from envo import venv_utils
from envium import (
    env_var,
    ctx_var,
    computed_env_var,
    computed_secret,
    computed_ctx_var,
    EnvGroup,
    CtxGroup,
    SecretsGroup,
    secret,
)
