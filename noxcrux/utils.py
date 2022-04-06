import logging


def disable_logging(function):

    def wrapper(*args, **kwargs):
        logging.disable()
        result = function(*args, **kwargs)
        logging.disable(logging.NOTSET)

        return result

    return wrapper
