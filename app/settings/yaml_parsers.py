import os
import string

import yaml

POSSIBLE_SYMBOLS_VALUES = {value for value in string.__all__ if isinstance(value, str)}


class YAMLStringValueError(yaml.YAMLError):
    def __init__(self, value):
        super().__init__(f"Can't parse string_module value: {value}")


class YAMLEnvVariableError(yaml.YAMLError):
    def __init__(self, value):
        super().__init__(f"Variable {value} does not exist")


def string_module_constructor(loader: yaml.Loader, node: yaml.Node) -> str:
    value = loader.construct_scalar(node)
    if value in POSSIBLE_SYMBOLS_VALUES:
        return getattr(string, value)
    raise YAMLStringValueError(value)


def env_constructor(loader: yaml.Loader, node: yaml.Node) -> str:
    value = loader.construct_scalar(node)
    if value not in os.environ:
        raise YAMLEnvVariableError(value)
    return os.environ.get(value)


def add_yaml_constructors() -> None:
    yaml.add_constructor('!string_module', string_module_constructor)
    yaml.add_constructor('!env', env_constructor)
