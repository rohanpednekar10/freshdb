import freshdb
import json

datastore = freshdb.get_instance(file_name="data")
key = "Fly"
value = {
    "value": "Mayflies"
}
ttl = 24 * 60 * 60 * 1000 # Time-To_Live set to 24 Hours

datastore.add(key, value, ttl=ttl)
print(json.dumps(datastore.get(key)), indent=1)