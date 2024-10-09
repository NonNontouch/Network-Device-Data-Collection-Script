import cv2
import numpy as np
from .config_handler import ConfigHandler
import src.error as Error


class text_to_pic:

    bg_color: tuple[int, int, int] = (0, 0, 0)
    text_color: tuple[int, int, int] = (255, 255, 255)
    font: int = cv2.FONT_HERSHEY_SIMPLEX
    font_scale: float = 1
    thickness: int = 2
    line_spacing: int = 8
    padding: int = 20
    font_map = {
        "FONT_HERSHEY_SIMPLEX": cv2.FONT_HERSHEY_SIMPLEX,
        "FONT_HERSHEY_PLAIN": cv2.FONT_HERSHEY_PLAIN,
        "FONT_HERSHEY_DUPLEX": cv2.FONT_HERSHEY_DUPLEX,
        "FONT_HERSHEY_COMPLEX": cv2.FONT_HERSHEY_COMPLEX,
        "FONT_HERSHEY_TRIPLEX": cv2.FONT_HERSHEY_TRIPLEX,
        "FONT_HERSHEY_COMPLEX_SMALL": cv2.FONT_HERSHEY_COMPLEX_SMALL,
        "FONT_HERSHEY_SCRIPT_SIMPLEX": cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
        "FONT_HERSHEY_SCRIPT_COMPLEX": cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
        "FONT_ITALIC": cv2.FONT_ITALIC,
    }

    def __init__(self) -> None:
        self.config = ConfigHandler("config.json")
        self.config.load_config()

        self.bg_color = (
            self.config.get("bg_color", self.bg_color) if self.config else self.bg_color
        )
        self.text_color = (
            self.config.get("text_color", self.text_color) if self.config else self.text_color
        )
        font_name = (
            self.config.get("font", "FONT_HERSHEY_SIMPLEX")
            if self.config
            else "FONT_HERSHEY_SIMPLEX"
        )
        self.font = self.font_map.get(
            font_name, self.font
        )  # Default font if not found in map
        self.font_scale = (
            self.config.get("font_scale", self.font_scale) if self.config else self.font_scale
        )
        self.thickness = (
            self.config.get("thickness", self.thickness) if self.config else self.thickness
        )
        self.line_spacing = (
            self.config.get("line_spacing", self.line_spacing)
            if self.config
            else self.line_spacing
        )
        self.padding = self.config.get("padding", self.padding) if self.config else self.padding

    def set_parameters(self, config: dict):
        """Set the configuration based on the provided dictionary."""
        # Map dictionary keys to instance variables
        for key, value in config.items():
            if hasattr(self, key):
                if key == "font":
                    value = self.font_map[value]

                setattr(self, key, value)
        self.save_config("config.json")

    def get_cur_config(self):
        return {
            "bg_color": self.bg_color,
            "text_color": self.text_color,
            "font": next(
                (key for key, value in self.font_map.items() if value == self.font),
                None,
            ),
            "font_scale": self.font_scale,
            "thickness": self.thickness,
            "line_spacing": self.line_spacing,
            "padding": self.padding,
        }

    def set_bg_color(self, bg_color: tuple[int, int, int]):
        self.bg_color = bg_color

    def set_text_color(self, text_color: tuple[int, int, int]):
        self.text_color = text_color

    def set_line_spacing(self, line_spacing: int):
        self.line_spacing = line_spacing

    def set_font_scale(self, font_scale: float):
        self.font_scale = font_scale

    def get_available_fonts(self):
        # List of OpenCV fonts
        return [
            "FONT_HERSHEY_SIMPLEX",
            "FONT_HERSHEY_PLAIN",
            "FONT_HERSHEY_DUPLEX",
            "FONT_HERSHEY_COMPLEX",
            "FONT_HERSHEY_TRIPLEX",
            "FONT_HERSHEY_COMPLEX_SMALL",
            "FONT_HERSHEY_SCRIPT_SIMPLEX",
            "FONT_HERSHEY_SCRIPT_COMPLEX",
            "FONT_ITALIC",
        ]

    def change_font(self, font_name: str):
        # Map font names to OpenCV font constants

        # Set the font if it exists in the map
        if font_name in self.font_map:
            self.font = self.font_map[font_name]
        else:
            print(f"Font '{font_name}' not found. Using default font.")

    def set_thickness(self, thickness: int):
        self.thickness = thickness

    def create_text_image(self, text: str):
        bg_color_bgr = (self.bg_color[2], self.bg_color[1], self.bg_color[0])
        text_color_bgr = (self.text_color[2], self.text_color[1], self.text_color[0])
        # Split the text into lines
        lines = text.splitlines()

        # Calculate the size of the text
        max_width = 0
        total_height = 0

        for line in lines:
            (line_width, line_height), baseline = cv2.getTextSize(
                line, self.font, self.font_scale, self.thickness
            )
            max_width = max(max_width, line_width)
            total_height += line_height + self.line_spacing  # Include line spacing

        # Set the width and height including padding
        width = max_width + 2 * self.padding
        height = total_height + 2 * self.padding

        # Create the image with the calculated size
        image = np.full((height, width, 3), bg_color_bgr, dtype=np.uint8)

        # Calculate the starting position for the first line
        y = (
            self.padding
            + total_height
            - (len(lines) * (line_height + self.line_spacing))
            + line_height
        )

        # Draw each line of text onto the image
        for line in lines:
            cv2.putText(
                image,
                line,
                (self.padding, y),
                self.font,
                self.font_scale,
                text_color_bgr,
                self.thickness,
            )
            y += line_height + self.line_spacing

        return image

    def save_config(self, file_path: str):
        """Save the current configuration to a JSON file, merging with existing settings."""

        # Prepare new configuration
        new_config = {
            "bg_color": self.bg_color,
            "text_color": self.text_color,
            "font": next(
                (key for key, value in self.font_map.items() if value == self.font),
                None,
            ),
            "font_scale": self.font_scale,
            "thickness": self.thickness,
            "line_spacing": self.line_spacing,
            "padding": self.padding,
        }

        # Update existing config with new config values
        self.config.save_config(new_config)
