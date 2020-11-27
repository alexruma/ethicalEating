import os
from json_handler import JSONHandler


def username_exists(username):
    path = os.path.join(os.path.dirname(__file__), 'resources', 'users.json')

    json = JSONHandler(path)
    json_dict = json.read_json()

    for key in json_dict:
        if username == key:
            return True

    return False


def auth_match(username, password):
    path = os.path.join(os.path.dirname(__file__), 'resources', 'users.json')

    json = JSONHandler(path)
    json_dict = json.read_json()

    if username_exists(username):
        if password == json_dict[username]["password"]:
            return True
    else:
        return False


def user_authentication(username, password):

    if auth_match(username, password):
        return True
    else:
        return False


def create_new_user(username, password):
    path = os.path.join(os.path.dirname(__file__), 'resources', 'users.json')

    json = JSONHandler(path)
    json_dict = json.read_json()

    json_dict.update({username: {"username": username,
                                 "password": password,
                                 "saved_recipes": [],
                                 "custom_recipe_keys": []}})

    json.write_json(json_dict)
