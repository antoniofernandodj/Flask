
from dynaconf import Dynaconf
from pathlib import Path
import os

PATH = str(Path(__file__).parent)

settings = Dynaconf(
    envvar_prefix="FLASK",
    settings_files=[
        os.path.join(PATH, 'settings.toml'),
        os.path.join(PATH, '.secrets.toml')
    ],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
