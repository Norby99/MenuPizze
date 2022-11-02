import json

def is_json(myjson):
    """
    Returns True if the json is valid
    """
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True
