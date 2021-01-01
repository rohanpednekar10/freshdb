import json
import os
import sys
import time
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor
from freshdb import config
from freshdb.utils import is_valid, is_live

class DataStore:
    def __init__(self, file_name, *args, **kwargs):
        self.__file_name = file_name
        self.__data = dict()
        self.__lock = threading.Lock()
        self.__executor = ThreadPoolExecutor(2)
        self._read()


    def _read(self):
        with open(self.__file_name, "r") as json_file:
            self.__data = json.load(json_file)


    def _write(self):
        with open(self.__file_name, "w") as json_file:
            json.dump(self.__data, json_file)

    def _post(self, key, value, ttl=None):
        data = {
            "value": value,
            "ttl": ttl,
            "timestamp": time.time()
        }

        if (sys.getsizeof(self.__data) + sys.getsizeof(data)) > config.MAX_FILE_STORAGE_SIZE:
            raise ValueError("File storage exceeding the {} limit.".format(config.MAX_FILE_STORAGE_SIZE))
        else:
            self.__data[key] = data
            loop = asyncio.get_event_loop()
            loop.run_in_executor(self.__executor, self._write)            


    def add(self, key, value, ttl=None):
        with self.__lock:
            if key in self.__data:
                raise ValueError("Key [{}] already present.".format(key))
            
            elif is_valid(key, value_type="key") and is_valid(value, value_type="value"):
                if ttl is not None:
                    try:
                        ttl = int(ttl)
                    except:
                        raise ValueError("Time-to-live {} must be an integer value.".format(ttl))

                self._post(key, value["value"], ttl=ttl)
            else:
                raise ValueError("Either provided key(allowed_size:{} characters) or value(allowed_size:{} bytes) doesn't meet the configuration.".format(config.MAX_KEY_LEN, config.MAX_VALUE_SIZE))

    
    def get(self, key):
        with self.__lock:
            if key not in self.__data:
                raise ValueError("Key [{}] not in datastore.".format(key))
            
            if is_live(self.__data[key]["ttl"], self.__data[key]["timestamp"]):
                response = {
                    "value": self.__data[key]["value"]   
                }
                return response
            else:
                self.delete(key)
    

    def delete(self, key):
        with self.__lock:
            if key not in self.__data:
                return
            del self.__data[key]
            loop = asyncio.get_event_loop()
            loop.run_in_executor(self.__executor, self._write)
