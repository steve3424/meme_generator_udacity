"""Class to encapsulate a quote as a body and author."""

class QuoteModel():
    """Class to represent a quote and author."""

    def __init__(self, quote, author):
        """Initialize quote object."""
        self.body = quote
        self.author = author

    def __str__(self):
        """Readable quote representation."""
        return self.body + " - " + self.author
