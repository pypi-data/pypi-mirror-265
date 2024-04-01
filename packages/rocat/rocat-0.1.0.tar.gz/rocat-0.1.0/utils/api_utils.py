# rocat/utils/api_util.py

api_key = None

def get_api_key():
    global api_key
    return api_key

def set_api_key(key):
    global api_key
    api_key = key