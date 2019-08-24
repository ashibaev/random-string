import pathlib
import logging
from typing import Any, Dict

import yaml

from app.settings.yaml_parsers import add_yaml_constructors
from app.settings.configs import app_config_from_dict, Config

PROJECT_ROOT: pathlib.Path = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT.parent / 'config' / 'app.yml'


def load_raw_config(data: str) -> Dict[str, Any]:
    add_yaml_constructors()
    try:
        config = yaml.load(data, Loader=yaml.Loader)
    except yaml.YAMLError as e:
        logging.error(f"Can not parse config: {e}")
        raise
    return config


def load_config(config_path=DEFAULT_CONFIG_PATH) -> Config:
    with open(config_path) as f:
        data = f.read()
    raw_config = load_raw_config(data)
    return app_config_from_dict(raw_config)
