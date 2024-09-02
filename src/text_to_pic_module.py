from PIL import Image, ImageDraw, ImageFont
from .error import Error


class text_to_pic:
    width: int
    height: int
    bg_color: tuple[float, ...] = (0, 0, 0)
    text_color: tuple[float, ...] = (0, 0, 0)
    font: ImageFont
    line_spacing: int = 5

    def set_width(self, width: int):
        if width <= 0:
            return
        self.width = width

    def set_height(self, height: int):
        if height <= 0:
            return
        self.height = height

    def set_bg_color(self, bg_color: tuple[float, ...]):
        self.bg_color = bg_color

    def set_text_color(self, text_color):
        self.text_color = text_color

    def set_text(self, text: str):
        self.text = text

    def set_line_spacing(self, line_spacing: int):
        self.line_spacing = line_spacing

    def set_font(self, font_path=None, font_size=24):
        try:
            if font_path == None:
                self.font = ImageFont.load_default(font_size)
            else:
                self.font = ImageFont.truetype(font_path, font_size)
        except OSError as e:
            raise Error.NoFontError(font_path) from e

    def create_text_image(self, text: str, padding=10, line_spacing=5):
        # Load a font

        # Create a drawing context to calculate text size
        dummy_image = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(dummy_image)

        # Split the text into lines
        lines = text.splitlines()

        # Calculate the maximum width and total height of the text
        max_width = max(
            draw.textbbox((0, 0), line, font=self.font)[2] for line in lines
        )
        total_height = sum(
            draw.textbbox((0, 0), line, font=self.font)[3]
            - draw.textbbox((0, 0), line, font=self.font)[1]
            for line in lines
        )

        # Calculate the image size, adding padding
        image_width = max_width + 2 * padding
        image_height = total_height + 2 * padding + (len(lines) - 1) * line_spacing

        # Create an image with the calculated size
        image = Image.new("RGB", (image_width, image_height), color=self.bg_color)
        draw = ImageDraw.Draw(image)

        # Draw the text on the image with padding
        y_offset = padding
        for line in lines:
            draw.text(
                xy=(padding, y_offset), text=line, font=self.font, fill=self.text_color
            )
            y_offset += (
                draw.textbbox(xy=(0, 0), text=line, font=self.font)[3]
                - draw.textbbox(xy=(0, 0), text=line, font=self.font)[1]
                + line_spacing
            )

        return image
