import sys
import time
import uuid
from freshdb import config

def is_valid(value, value_type = "key"):
    if value_type.lower() == "key":
        if not isinstance(value, str):
            raise ValueError("Key [{}] must be of type string.".format(value))
        return len(value) <= config.MAX_KEY_LENGTH
    elif value_type.lower() == "value":
        if isinstance(value, dict):
            return sys.getsizeof(value) <= config.MAX_VALUE_SIZE
        raise ValueError("Value [{}] must be of type dictionary.".format(value))


def is_live(ttl, timestamp):
    if ttl is None:
        return True
    current_time = int(time.time() * 1000)
    return (current_time - timestamp) > (ttl * 1000)


def get_file_name():
    file_name = uuid.uuid4().hex
    return file_name
