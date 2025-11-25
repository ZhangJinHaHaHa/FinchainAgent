import hashlib
import json
import time

def calculate_hash(data: dict) -> str:
    """Calculates the SHA256 hash of a dictionary."""
    json_str = json.dumps(data, sort_keys=True)
    return hashlib.sha256(json_str.encode('utf-8')).hexdigest()

def get_timestamp() -> str:
    """Returns current timestamp."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
