import json
import os

import src.error as Error


class json_file:
    file_list: set
    os_template: dict

    def get_list_of_file(self):
        folder_path = os.path.abspath(os.path.join("command_template"))

        try:
            self.file_list = os.listdir(folder_path)
            return self.file_list
        except FileNotFoundError:
            print(f"Error: Folder '{folder_path}' not found.")
            raise Error.JsonFileNotFound(folder_path)

    def read_json_file(self, file_name: str):
        self.__focused_file = file_name
        file_path = os.path.abspath(os.path.join("command_template", file_name))

        try:
            with open(file_path, "r") as f:
                self.os_template = json.load(f)
                return self.os_template
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            raise Error.JsonFileNotFound(file_path)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file '{file_path}'.")
            raise Error.InvalidJsonFile(file_path)

    def get_command_json(self, OS: str):
        """Return commands without altering regex data."""
        try:
            self.read_json_file(self.__focused_file)
            os_data = self.os_template[OS]
            # Return only the command data while preserving regex
            command_data = {
                key: value for key, value in os_data.items() if key != "regex"
            }
            return command_data
        except (KeyError, FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error getting command list for OS {OS}: {e}")
            raise Error.JsonOSTemplateError(OS)

    def get_os_keys(self):
        if isinstance(self.os_template, dict):
            return list(self.os_template.keys())
        return []

    def set_new_command(self, os_template):
        self.os_template = os_template

    def write_json_file(self, file_name: str):
        folder_path = os.path.abspath(os.path.join("command_template"))
        if not os.path.exists(folder_path):
            print(f"Creating directory: {folder_path}")
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    existing_data = json.load(f)
            else:
                existing_data = {}

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            raise Exception("JsonFileNotFound", file_path)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file '{file_path}'.")
            raise Exception("InvalidJsonFile", file_path)

        # Function to update existing nested dictionaries without overwriting
        def deep_update(source, updates):
            for key, value in updates.items():
                if isinstance(value, dict) and key in source:
                    source[key] = deep_update(source[key], value)
                else:
                    source[key] = value
            return source

        # Update existing data with os_template without overwriting nested structures like "regex"
        updated_data = deep_update(existing_data, self.os_template)

        # Sort the existing data by OS keys before writing it back
        sorted_data = dict(sorted(updated_data.items()))

        try:
            with open(file_path, "w") as f:
                json.dump(sorted_data, f, indent=4)
                print(f"Successfully modified {file_path}")
        except Exception as e:
            print(f"Error writing to file '{file_path}': {e}")

    def get_regex(self, OS: str):
        """Retrieve the regex for the specified OS."""
        try:
            self.read_json_file(self.__focused_file)
            os_data = self.os_template[OS]
            return os_data.get("regex", {})  # Return the regex object if exists
        except (KeyError, FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error getting regex for OS {OS}: {e}")
            raise Error.JsonOSTemplateError(OS)
