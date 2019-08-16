import os
import string

import yaml

POSSIBLE_SYMBOLS_VALUES = {value for value in string.__all__ if isinstance(value, str)}


class IncorrectYAMLStringValue(yaml.YAMLError):
    pass


def string_module_constructor(loader: yaml.Loader, node: yaml.Node) -> str:
    value = loader.construct_scalar(node)
    if value in POSSIBLE_SYMBOLS_VALUES:
        return getattr(string, value)
    raise IncorrectYAMLStringValue(f"Can't parse string_module value: {value}")


def env_constructor(loader: yaml.Loader, node: yaml.Node) -> str:
    value = loader.construct_scalar(node)
    return os.environ.get(value, '')


def add_yaml_constructors() -> None:
    yaml.add_constructor('!string_module', string_module_constructor)
    yaml.add_constructor('!env', env_constructor)
