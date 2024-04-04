import json
import os


class MockAI:

    def __init__(self):
        self.config = {}
        self.commands = {}


    def set_config(self, json_file_path: str):
        # Check if the file exists
        config_path = os.path.join(os.getcwd(), json_file_path)
        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"The specified JSON file was not found: {json_file_path}")

        # Read the json file and set the configuration
        with open(config_path, 'r') as json_file:
            try:
                config_data = json.load(json_file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON file: {e}")
        # save the config for later
        self.config = config_data
        self.commands = self._get_commands()

    def _get_commands(self):
        commands = {}
        for k,v in self.config.items():
            with open(v, 'r') as json_file:
                try:
                    value = json.load(json_file)
                    commands[k] = value
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON file: {e}")
        return commands



    def get_completion(self, message:str):
        return self.commands.get(message.strip())