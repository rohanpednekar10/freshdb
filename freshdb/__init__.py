import fcntl
import json
import os
from freshdb import config
from freshdb.utils import get_file_name
from freshdb.models import DataStore

def get_instance(file_path = None, file_name = None):
    if file_path is None:
        file_path = config.DEFAULT_FILE_PATH

    if file_name is None:
        file_name = get_file_name()
    else:
        file_name = file_name.split(".", 1)[0]

    full_file_name = "{}{}.json".format(file_path, file_name)
    file_descriptor = os.open(full_file_name, os.O_CREAT | os.O_RDWR)
    
    try:
        print("Acquiring file lock on {}...".format(file_name))
        fcntl.flock(file_descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise BlockingIOError("Resource '{}' is already locked'".format(file_name))
    except Exception:
        raise
    else:
        print("File lock acquired on {}!".format(file_name))

    if not os.path.isfile(full_file_name) or os.fstat(file_descriptor).st_size == 0:
        with open(full_file_name, 'w') as json_file:
            json.dump({}, json_file)
  
    return DataStore(full_file_name)

__all__ = ['get_instance']

