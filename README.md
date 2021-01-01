# **FreshDB**

## **Description**

File-based key-value data store that supports the basic CRD (Create, Read and Delete) operations.

<br>

## **Features**

1. It can be initialized using an optional file path and file name. If not provided, it will reliably create itself using `uuid` in the default file path.
2. Key string capped at 32 characters and Value must be a JSON object capped at 16KB. (These values can be changed in *config.py*)
3. Every key supports setting a Time-To-Live aka ttl property when it is created. This property is optional. If provided, it will be evaluated as an integer defining the number of seconds. Once the Time-To-Live for a key has expired, the key will no longer be available for Read or Delete operations.
4. Only one process can access the data store at a time.
5. Data store is thread-safe.

<br>

## **Usage**

<br>

**Create an instance**

```python

import freshdb

datastore = freshdb.get_instance(file_path=None, file_name=None)

```

Note: When `file_path` and `file_name` is provided in the get_instance() call, it will obtain lock on that file using `fcntl`. If object is created for the same file path twice, `BlockingIOError` is thrown.

<br>

**Add Key-Value**

```python

key = "Whiteflies"
value = {
    "value": "Mayflies"
}
ttl = 24 * 60 * 60 * 1000

datastore.add(key, value, ttl=ttl)

```

Note: `ttl` should be of type `int`. It represents Time-To-Live property in milliseconds.

<br>

**Get Value**

```python

key = "Whiteflies"

print(datastore.get(key))

```

<br>

**Delete Key-Value**

```python

key = "Whiteflies"

datastore.delete(key)

```

<br>

## **OS Support**
This package only works for Unix/Linux. 