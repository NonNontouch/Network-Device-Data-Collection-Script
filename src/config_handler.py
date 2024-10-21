import json
import os


class ConfigHandler:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = {}

        self.load_config()

    def load_config(self):
        """Load configuration from the specified JSON file."""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as config_file:
                self.config = json.load(config_file)
        else:

            self.save_config({})

    def save_config(self, new_config=None):
        """Save the current configuration to the JSON file, merging with existing settings."""

        existing_config = {}
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as config_file:
                existing_config = json.load(config_file)

        if new_config is not None:
            existing_config.update(new_config)

        with open(self.config_path, "w") as config_file:
            json.dump(existing_config, config_file, indent=4)

    def get(self, key, default=None):
        """Get a configuration value with an optional default."""
        return self.config.get(key, default)

    def set(self, key, value):
        """Set a configuration value and save to the file."""
        self.config[key] = value
        self.save_config({key: value})

    def get_all(self):
        """Return the entire configuration as a dictionary."""
        return self.config
