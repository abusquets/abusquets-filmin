import logging.config
import os

import yaml

from config import settings


APP_ENV = os.getenv('APP_ENV', 'dev')


def setup_logging():
    path = f'logging.{settings.APP_ENV}.yaml'
    with open(path, 'rt') as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)
