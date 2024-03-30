import json
import os
import pickle
from pathlib import Path


def load(path: os.PathLike, default=None):
    path = Path(path)
    if not path.suffix in ('.pickle', '.json'):
        raise ValueError('path must end in either .pickle or .json.')

    if path.exists():
        if path.suffix == '.pickle':
            with open(path, 'rb') as f:
                return pickle.load(f)
        elif path.suffix == '.json':
            with open(path) as f:
                return json.load(f)
    elif default is not None:
        return default

    raise FileNotFoundError('File not found and default==None.')


def dump(value, path: os.PathLike):
    path = Path(path)
    if path.suffix == '.pickle':
        with open(path, 'wb') as f:
            pickle.dump(value, f)
    elif path.suffix == '.json':
        with open(path, 'w') as f:
            json.dump(value, f)
    else:
        raise ValueError('path must end in either .pickle or .json.')
