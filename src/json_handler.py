import json
import os


class json_file:
    file_list: set
    os_template: dict
    command_list: list
    command_list_json: dict

    def get_list_of_file(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the absolute path to the command_template folder
        folder_path = os.path.join(current_dir, "..", "command_template")

        try:
            # List files in the command_template directory
            self.file_list = os.listdir(folder_path)
        except FileNotFoundError:
            print(f"Error: Folder '{folder_path}' not found.")
            return

    def read_json_file(self, file_name: str):
    # Get the absolute path of the current file's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construct the absolute path to the command_template folder and the specific JSON file
        file_path = os.path.join(current_dir, '..', 'command_template', file_name)
        
        try:
            with open(file_path, "r") as f:
                self.os_template = json.load(f)
                return self.os_template
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file '{file_path}'.")
            return None

    def get_command_json(self, OS: str):
        try:
            return self.os_template[OS]
        except (KeyError, FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error getting command list for OS {OS}: {e}")
            return None
