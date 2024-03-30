from pathlib import Path
from filelock import Timeout, FileLock
import doy.data as data
import pprint

_kvstore_basepath = "~/.doy_kvstore"
_kvstore_path = Path(_kvstore_basepath + ".pickle").expanduser()
_kvstore_hr_path = Path(_kvstore_basepath + ".hr").expanduser()
_kvstore_lock_path = Path(_kvstore_basepath + ".lock").expanduser()
lock = FileLock(_kvstore_lock_path)


@lock
def _try_write_hr_store(store):
    try:
        s = pprint.pformat(store, indent=4, width=120)
    except Exception as e:
        s = f"An error occurred while writing the human-readable representation of the store: {e}"
    with open(_kvstore_hr_path, "w") as f:
        f.write(s)


@lock
def get_store() -> dict:
    return data.load(_kvstore_path, default={})


@lock
def set_store(store: dict):
    data.dump(store, _kvstore_path)
    _try_write_hr_store(store)


@lock
def get(key):
    store = get_store()
    return store[key]


@lock
def set(key, value):
    store = get_store()
    store[key] = value
    set_store(store)
