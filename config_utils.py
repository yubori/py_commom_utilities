import os
import codecs
import unicodedata
import logging
from configparser import ConfigParser, ExtendedInterpolation


__LOGGER__ = logging.getLogger('config_utils')


def build_empty_config():
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.optionxform = str  # enable capital letters
    return config


def dump_config(config):
    entries = []
    for section in config.sections():
        for key in config[section]:
            entries.append("{}:{}:{}".format(section, key, config[section][key]))
    return '\n'.join(entries)


def load_config(file_path="config.ini", default_config=None):
    if default_config is None:
        config = ConfigParser()
    else:
        assert isinstance(default_config, ConfigParser)
        config = default_config

    if not os.path.exists(file_path):
        __LOGGER__.warning(f'Config file "{file_path}" is not found, '
                           f'use default settings {dump_config(default_config)}')
    else:
        config.read(file_path, encoding='utf-8')

    return normalize_config(config)


def save_config(config, file_path="config.ini"):
    assert isinstance(config, ConfigParser)
    config = normalize_config(config)
    with codecs.open(file_path, 'w', 'utf8') as configfile:
        config.write(configfile)

    return config


def normalize_config(config):
    assert isinstance(config, ConfigParser)
    n_config = ConfigParser(interpolation=ExtendedInterpolation())
    n_config.optionxform = str  # enable capital letters
    for section in config.sections():
        n_section = unicodedata.normalize('NFC', section)
        if n_section not in n_config:
            n_config[n_section] = {}

        for key in config[section]:
            n_key = unicodedata.normalize('NFC', key)
            n_config[n_section][n_key] = unicodedata.normalize('NFC', config[section][key])
    return n_config
