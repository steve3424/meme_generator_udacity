"""Command line tool for generating memes."""

import os
import random
from argparse import ArgumentParser
from QuoteEngine import Ingestor, QuoteModel
from MemeGenerator import MemeEngine


def generate_meme(path=None, body=None, author=None):
    """Generate a meme given an path and a quote."""
    img = None
    quote = None

    if path is None:
        images_path = "./data/photos/"
        imgs = []
        for root, dirs, files in os.walk(images_path):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quotes_path = "./data/quotes/"
        quote_files = []
        for root, dirs, files in os.walk(quotes_path):
            quote_files = [os.path.join(root, name) for name in files]

        quotes = []
        ingestor = Ingestor.Ingestor()
        for f in quote_files:
            quotes.extend(ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel.QuoteModel(body, author)

    meme = MemeEngine.MemeEngine('./static')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image
    parser = ArgumentParser(
        description="Optionally pass img path, quote body, and author to create meme")
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="path to image file")
    parser.add_argument("--body", type=str, default=None, help="quote body")
    parser.add_argument(
        "--author",
        type=str,
        default=None,
        help="author of quote")

    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
