import json

from typing import Dict

class Config:
    _config = {}
    
    def __init__(self, config_name, config_path):
        self._config[config_name] = self.load_config(config_path)

    def get_config(self, config_name):
        return self._config.get(config_name, {})

    def get_property(self, config_name, property):
        return self.get_config(config_name).get(property)

    def load_config(self, config_path: str) -> Dict[str, str]:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            config_file.close()
            return config
