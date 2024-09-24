import json
import os
import src.error as Error


class json_file:
    file_list: set
    os_template: dict

    def get_list_of_file(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the absolute path to the command_template folder
        folder_path = os.path.join(current_dir, "..", "command_template")

        try:
            # List files in the command_template directory
            self.file_list = os.listdir(folder_path)
        except FileNotFoundError:
            print(f"Error: Folder '{folder_path}' not found.")
            raise Error.JsonFileNotFound(folder_path)

    def read_json_file(self, file_name: str):
        # Get the absolute path of the current file's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the absolute path to the command_template folder and the specific JSON file
        file_path = os.path.join(current_dir, "..", "command_template", file_name)

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
        try:
            return self.os_template[OS]
        except (KeyError, FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error getting command list for OS {OS}: {e}")
            raise Error.JsonOSTemplateError(OS)

    def get_os_keys(self):
        """Return a list of OS keys from the loaded OS template."""
        if isinstance(self.os_template, dict):
            return list(self.os_template.keys())
        return []
