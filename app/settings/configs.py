from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class StringGeneratorConfig:
    length: int
    symbols: str


@dataclass
class Config:
    string_generator: StringGeneratorConfig
    update_interval: float
    logging: Dict[str, Any]


def _merge_symbols(strings: List[str]) -> str:
    return ''.join(sorted(set(letter for symbols_string in strings for letter in symbols_string)))


def string_generator_config_from_dict(d: Dict[str, Any]) -> StringGeneratorConfig:
    return StringGeneratorConfig(
        d['length'],
        _merge_symbols(d['symbols'])
    )


def app_config_from_dict(d: Dict[str, Any]) -> Config:
    return Config(
        string_generator_config_from_dict(d['string_generator']),
        d['update_interval'],
        d['logging']
    )
