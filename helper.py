"""
A collection of helpful functions.
"""
import os
import pickle

def save(data, name):
    """
    Serialises data
    Args:
        data - python data type
        name - used to create file name for serialised object
    """
    with open(_get_full_path(name), 'wb') as f:
        pickle.dump(data, f)

def load(name):
    """
    Deserialises data

    Args:
        name - used to create file name for deserialising object
    Returns: data
    """
    with open(_get_full_path(name), 'rb') as f:
        return pickle.load(f)

def _get_full_path(name):
    savedir = os.environ["HOME"] + '/.meetingbot/'
    return "".join([savedir, name, '.pickle'])
