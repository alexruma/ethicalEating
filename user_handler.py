import os
from json_handler import JSONHandler


def read_json():
    path = os.path.join(os.path.dirname(__file__), 'resources', 'users.json')

    json = JSONHandler(path)
    json_dict = json.read_json()

    return json_dict


def write_json(json_dict):
    path = os.path.join(os.path.dirname(__file__), 'resources', 'users.json')

    json = JSONHandler(path)
    json.write_json(json_dict)


def username_exists(username):
    json_dict = read_json()

    for key in json_dict:
        if username == key:
            return True

    return False


def auth_match(username, password):
    json_dict = read_json()

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
    json_dict = read_json()

    json_dict.update({username: {"username": username,
                                 "password": password,
                                 "recipe_keys": {},
                                 "custom_recipe_keys": {}}})

    write_json(json_dict)


def save_user_recipe(username, recipe_key, recipe_name):
    json_dict = read_json()

    json_dict[username]["recipe_keys"].update({recipe_key: recipe_name})

    write_json(json_dict)


def save_user_custom_recipe(username, recipe_key, recipe_name, ingredient_string):
    json_dict = read_json()

    ingredient_dict = eval(ingredient_string)

    ingredient_list = list(ingredient_dict.keys())

    json_dict[username]["custom_recipe_keys"].update({recipe_key: recipe_name})
    json_dict[username].update({recipe_key: ingredient_list})

    write_json(json_dict)


def remove_recipe(username, recipe_key):
    json_dict = read_json()

    del json_dict[username]["recipe_keys"][recipe_key]

    write_json(json_dict)


def remove_custom_recipe(username, recipe_key):
    json_dict = read_json()

    del json_dict[username]["custom_recipe_keys"][recipe_key]
    del json_dict[username][recipe_key]

    write_json(json_dict)


def load_saved_recipes(username):
    json_dict = read_json()
    keys = json_dict[username]["recipe_keys"]

    return keys


def load_custom_saved_recipes(username):
    json_dict = read_json()
    keys = json_dict[username]["custom_recipe_keys"]

    return keys


def load_custom_recipe_ingredients(username, key):
    json_dict = read_json()

    recipe = json_dict[username][key]

    ingredient_json_path = os.path.join(os.path.dirname(__file__), 'resources', 'ingredients.json')
    dict_of_ingredients = {}

    ingredient_json = JSONHandler(ingredient_json_path)
    ingredient_json_dict = ingredient_json.read_json()

    for key in recipe:
        dict_of_ingredients.update({key: ingredient_json_dict[key]["Display Name"]})

    return dict_of_ingredients
