import json
import pickle

def pickle_load(path):
    with open(path, 'rb') as handle:
        return pickle.load(handle)

def json_load(path):
    with open(path, 'r') as openfile:
        return json.load(openfile)
