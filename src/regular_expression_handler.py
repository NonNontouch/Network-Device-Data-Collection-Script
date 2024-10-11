import json
import re


class data_handling:
    def __init__(self, config_file: str):
        self.load_regex_config(config_file)

    def load_regex_config(self, config_file: str):
        """Load regular expressions from a configuration file."""
        try:
            with open(config_file, "r") as f:
                regex_config = json.load(f)

            self.check_error_regex = regex_config.get(
                "check_error",
                r"Invalid input|command not found|Unrecognized|Unknown command|Incomplete command|Illegal command|Error: Value out of range|Illegal parameter",
            )
            self.remove_control_char_regex = regex_config.get(
                "remove_control_char", r"[^\x20-\x7E\r\n]"
            )
            self.is_ready_input_username_regex = regex_config.get(
                "is_ready_input_username",
                r"(?:login|username|user)(?!.*password:pass|Password)",
            )
            self.is_ready_input_password_regex = regex_config.get(
                "is_ready_input_password",
                r"(?:password:pass|Password)(?!.*login|username|user)",
            )
            self.remove_more_keyword_regex = regex_config.get(
                "remove_more_keyword", r"--[Mm]ore--"
            )

        except FileNotFoundError:
            print(f"Error: Configuration file '{config_file}' not found.")
            self.set_default_regexes()  # Optionally set default regexes
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in the configuration file '{config_file}'.")
            self.set_default_regexes()  # Optionally set default regexes

    def set_default_regexes(self):
        """Set default regex values if loading fails."""
        self.find_prompt_regex = r"^\s*([\w-]+)(>|#)\s*$"
        self.check_error_regex = r"Invalid input|command not found|Unrecognized|Unknown command|Incomplete command|Illegal command|Error: Value out of range|Illegal parameter"
        self.remove_control_char_regex = r"[^\x20-\x7E\r\n]"
        self.is_ready_input_username_regex = (
            r"(?:login|username|user)(?!.*password:pass|Password)"
        )
        self.is_ready_input_password_regex = (
            r"(?:password:pass|Password)(?!.*login|username|user)"
        )
        self.remove_more_keyword_regex = r"--[Mm]ore--"

    def find_prompt(self, output: str, regex: str = r"^\s*([\w-]+)(>|#)\s*$"):
        if output:
            last_line = output.splitlines()[-1].strip()
            if re.match(regex, last_line):
                return True
        return False

    def check_error(self, output: str):
        return (
            re.search(self.check_error_regex, output, flags=re.IGNORECASE) is not None
        )

    def remove_control_char(self, command_output: str):
        return re.sub(
            self.remove_control_char_regex,
            "",
            re.sub(r"\x1B[@-_][0-?]*[ -/]*[@-~]", "", command_output),
        )

    def is_ready_input_username(self, telnet_output: str):
        return (
            re.search(
                self.is_ready_input_username_regex, telnet_output, flags=re.IGNORECASE
            )
            is not None
        )

    def is_ready_input_password(self, telnet_output: str):
        return (
            re.search(
                self.is_ready_input_password_regex, telnet_output, flags=re.IGNORECASE
            )
            is not None
        )

    def remove_more_keyword(self, output: str):
        return re.sub(self.remove_more_keyword_regex, "", output)

    def ends_with(self, output: str, ending: str) -> bool:
        """Check if the output string ends with the specified ending character."""
        # Construct the regex pattern
        pattern = rf"\s*{re.escape(ending)}\s*$"

        # Match the pattern against the output
        return bool(re.search(pattern, output))
