import json


class JSONHandler:
    """
    Class to interact with JSON. To iniatilize a path to the JSON needs to be passed (i.e. resources/ingredients.json)
    """

    def __init__(self, path: str):
        self.path = path

    def read_json(self):

        with open(self.path, 'r') as file_json:
            loaded_json = json.load(file_json)

        return loaded_json

    def write_json(self, output: dict):

        with open(self.path, 'w') as updated_json:
            json.dump(output, updated_json, indent=4)
