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
            # Create the config file with an empty dictionary if it doesn't exist
            self.save_config({})  # Save an empty config initially

    def save_config(self, new_config=None):
        """Save the current configuration to the JSON file, merging with existing settings."""
        # Load existing configuration
        existing_config = {}
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as config_file:
                existing_config = json.load(config_file)

        # Update existing config with new config values
        if new_config is not None:
            existing_config.update(new_config)

        # Write the updated configuration back to the file
        with open(self.config_path, "w") as config_file:
            json.dump(existing_config, config_file, indent=4)

    def get(self, key, default=None):
        """Get a configuration value with an optional default."""
        return self.config.get(key, default)

    def set(self, key, value):
        """Set a configuration value and save to the file."""
        self.config[key] = value
        self.save_config({key: value})  # Save the specific key's new value

    def get_all(self):
        """Return the entire configuration as a dictionary."""
        return self.config
