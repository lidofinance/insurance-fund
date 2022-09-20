import sys
import os

import utils.log as log


def get_env(name):
    return os.getenv(name)


def check_env_var(variable, display=True, prompt=True):
    log.info(f"Checking `{variable}`...")

    value = get_env(variable)

    if value:
        log.okay(variable, value if display else mask(value))
        log.proceed()
    else:
        log.error(f"`{variable}` not found!")
        log.proceed()

    return value


def mask(text):
    return len(text[:-4]) * "#" + text[-4:]

