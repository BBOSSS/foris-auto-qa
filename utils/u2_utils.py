import time
from retry.api import retry_call

from utils.decorator import exception_to_bool


@exception_to_bool
def check_exists(phone, tries=5, delay=1, **kwargs):
    result = retry_call(_check_exists, fargs=[phone], fkwargs=kwargs, tries=tries, delay=delay)
    return result


def _check_exists(phone, **kwargs):
    if phone(**kwargs).exists():
        return True
    else:
        raise Exception(f"element not exists: {kwargs}")


def click_wait(phone, wait=2, **kwargs):
    phone(**kwargs).click()
    time.sleep(wait)


@exception_to_bool
def scroll_check_exists(phone, direction, tries=5, delay=1, **kwargs):
    """
    direction: one of "left", "right", "up", "bottom" or Direction.LEFT
    """
    result = retry_call(_scroll_check_exists, fargs=[phone, direction],
                        fkwargs=kwargs, tries=tries, delay=delay)
    return result


def _scroll_check_exists(phone, direction, **kwargs):
    if phone(**kwargs).exists():
        return True
    else:
        phone.swipe_ext(direction)
        raise Exception(f"element not exists: {kwargs}")
