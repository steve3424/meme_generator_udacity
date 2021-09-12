"""Starts flask server to send and receive http requests for generating memes."""

import random
import os
import requests
from flask import Flask, render_template, abort, request

from QuoteEngine import Ingestor, QuoteModel
from MemeGenerator import MemeEngine

app = Flask(__name__)

meme = MemeEngine.MemeEngine('./static')


def setup():
    """Load all resources."""
    quotes_path = "./data/quotes/"
    quote_files = []
    for root, dirs, files in os.walk(quotes_path):
        quote_files = [os.path.join(root, name) for name in files]

    quotes = []
    ingestor = Ingestor.Ingestor()
    for qf in quote_files:
        quotes.extend(ingestor.parse(qf))

    images_path = "./data/photos/"
    imgs = []
    for root, dirs, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)

@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""
    img_url = request.form["image_url"]
    quote = QuoteModel.QuoteModel(request.form["body"], request.form["author"])
    img = requests.get(img_url)
    temp_path = f"./tmp/{random.randint(0, 100000)}.png"
    with open(temp_path, 'wb') as f:
        f.write(img.content)

    path = meme.make_meme(temp_path, quote.body, quote.author)

    os.remove(temp_path)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
