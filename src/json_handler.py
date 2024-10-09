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
            return self.file_list
        except FileNotFoundError:
            print(f"Error: Folder '{folder_path}' not found.")
            raise Error.JsonFileNotFound(folder_path)

    def read_json_file(self, file_name: str):
        self.__focused_file = file_name
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
            self.read_json_file(self.__focused_file)
            return self.os_template[OS]
        except (KeyError, FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error getting command list for OS {OS}: {e}")
            raise Error.JsonOSTemplateError(OS)

    def get_os_keys(self):
        """Return a list of OS keys from the loaded OS template."""
        if isinstance(self.os_template, dict):
            return list(self.os_template.keys())
        return []

    def set_new_command(self, os_template):
        self.os_template = os_template

    def write_json_file(self, file_name: str):
        """Modify the current os_template in the existing JSON file."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(current_dir, "..", "command_template")

        # Ensure the folder exists
        if not os.path.exists(folder_path):
            print(f"Creating directory: {folder_path}")
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, file_name)

        # Load the existing data from the file if it exists
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    existing_data = json.load(f)
            else:
                existing_data = {}  # Create an empty dictionary if file does not exist
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            raise Error.JsonFileNotFound(file_path)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file '{file_path}'.")
            raise Error.InvalidJsonFile(file_path)

        # Update the existing data with the new os_template
        existing_data.update(self.os_template)

        # **Sort the existing data by OS keys before writing it back**
        sorted_data = dict(sorted(existing_data.items()))  # <--- New sorting logic

        # Write the sorted data back to the same file
        try:
            with open(file_path, "w") as f:
                json.dump(sorted_data, f, indent=4)  # Use sorted data here
                print(f"Successfully modified {file_path}")
        except Exception as e:
            print(f"Error writing to file '{file_path}': {e}")
            raise Error.WriteProbJonFile(file_path)
