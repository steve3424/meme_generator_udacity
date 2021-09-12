"""Class for generating meme from img url and quote using pillow library."""

import textwrap
from PIL import Image, ImageDraw, ImageFont
import random
import os


class MemeEngine():
    """Class for creating a meme out of a quote, author, and image."""

    def __init__(self, output_dir):
        """Initialize MemeEngine with output dir for generated meme."""
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def make_meme(self, img_path, quote_body, quote_author, width=500):
        """Create meme out of image, quote body, author, and optional img width."""
        img = Image.open(img_path)

        w, h = img.size
        width = min(width, 500)
        resize_ratio = width / w
        height = int(resize_ratio * h)
        img = img.resize((width, height), Image.NEAREST)

        font = ImageFont.truetype('./data/fonts/Urbanist-Bold.ttf', size=25)
        wrapper = textwrap.TextWrapper(width=25)
        words = wrapper.wrap(text=quote_body)
        new_quote = ""
        for w in words[:-1]:
            new_quote = new_quote + w + '\n'
        new_quote += words[-1]

        draw = ImageDraw.Draw(img)
        draw.text((10, 10), new_quote, font=font, fill="black")
        draw.text(
            (10,
             height - 35),
            f" - {quote_author}",
            font=font,
            fill="black")

        output_path = os.path.join(
            self.output_dir,
            f"{random.randint(1, 100000)}.png")
        img.save(output_path)
        return output_path
