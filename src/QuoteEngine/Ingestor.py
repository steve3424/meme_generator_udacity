"""Classes and interface for parsing different file formats for quotes."""

import random
import subprocess
from abc import ABC, abstractmethod
import os
import docx
import csv
from QuoteEngine.QuoteModel import QuoteModel


class IngestorInterface(ABC):
    """Base class to be used as the interface for specific ingestors."""

    @property
    @abstractmethod
    def supported_file_type(self):
        """Return doc type supported by ingestor."""
        pass

    @abstractmethod
    def parse(self, path):
        """Handle the parsing of the specified file."""
        pass

    def can_parse(self, path):
        """Return a boolean value indicating whether or not this ingestor can handle the given file type."""
        extension = path.split('.')[-1]
        if extension == self.supported_file_type:
            return True
        return False


class PDFIngestor(IngestorInterface):
    """Parse text in a PDF file."""

    @property
    def supported_file_type(self):
        """Return pdf as supported file type."""
        return "pdf"

    def parse(self, path):
        """Parse text from PDF using pdftotext as a subprocess and returns list of quote models."""
        if not os.path.exists("./tmp"):
            os.makedirs("./tmp")
        temp_file = f"./tmp/temp_{random.randint(0, 100000)}.txt"
        subprocess.call(["pdftotext", "-layout", path, temp_file])

        quotes = []
        with open(temp_file, "r") as f:
            for line in f.readlines():
                line = line.strip("\n\r").strip()
                if len(line) > 0:
                    parsed_line = line.split(" - ")
                    quotes.append(QuoteModel(parsed_line[0].strip("\""),
                                             parsed_line[1]))

        os.remove(temp_file)
        return quotes

    def __str__(self):
        """Return the string representation of doc type this ingestor handles."""
        return ".pdf"


class TXTIngestor(IngestorInterface):
    """Parse quotes in a TXT file."""

    @property
    def supported_file_type(self):
        """Return txt as supported file type."""
        return "txt"

    def parse(self, path):
        """Parse text from TXT file and returns list of quote models."""
        quotes = []
        with open(path, "r") as f:
            for line in f.readlines():
                parsed_line = line.split(" - ")
                quotes.append(QuoteModel(parsed_line[0].strip("\r\n\""),
                                         parsed_line[1].strip("\r\n")))
        return quotes

    def __str__(self):
        """Return the string representation of doc type this ingestor handles."""
        return ".txt"


class DOCXIngestor(IngestorInterface):
    """Parse quotes in a DOCX file."""

    @property
    def supported_file_type(self):
        """Return docx as supported file type."""
        return "docx"

    def parse(self, path):
        """Parse text from DOCX file and returns list of quote models."""
        quotes = []
        doc = docx.Document(path)
        for p in doc.paragraphs:
            p_stripped = p.text.strip()
            if len(p_stripped) > 0:
                parsed_line = p_stripped.split(" - ")
                quotes.append(QuoteModel(parsed_line[0].strip("\""),
                                         parsed_line[1]))
        return quotes

    def __str__(self):
        """Return the string representation of doc type this ingestor handles."""
        return ".docx"


class CSVIngestor(IngestorInterface):
    """Parses quotes in a CSV file."""

    @property
    def supported_file_type(self):
        """Return csv as supported file type."""
        return "csv"

    def parse(self, path):
        """Parse text from csv file and returns list of quote models."""
        quotes = []
        with open(path, "r") as f:
            d = csv.DictReader(f)
            for row in d:
                quotes.append(QuoteModel(row['body'],
                                         row['author']))
        return quotes

    def __str__(self):
        """Return the string representation of doc type this ingestor handles."""
        return ".csv"


class CSVIngestor(IngestorInterface):
    """Parse quotes in a CSV file."""

    @property
    def supported_file_type(self):
        """Return csv as supported file type."""
        return "csv"

    def parse(self, path):
        """Parse text from csv file and returns list of quote models."""
        quotes = []
        with open(path, "r") as f:
            d = csv.DictReader(f)
            for row in d:
                quotes.append(QuoteModel(row['body'],
                                         row['author']))
        return quotes

    def __str__(self):
        """Return the string representation of doc type this ingestor handles."""
        return ".csv"


class Ingestor():
    """Parser class which is the user interface for parsing files."""

    def __init__(self):
        """Initialize list of available ingestors."""
        self.ingestors = [
            PDFIngestor(),
            TXTIngestor(),
            DOCXIngestor(),
            CSVIngestor()]

    def parse(self, path):
        """Find ingestor to parse file type and return list of quotes."""
        for ingestor in self.ingestors:
            if ingestor.can_parse(path):
                return ingestor.parse(path)
        raise Exception(f"Parser not found for doc type {path.split('.')[-1]}")
        return []

    def __str__(self):
        """Human readable representation of ingestor."""
        file_types = []
        for p in self.ingestors:
            file_types.append(str(p))
        return f"Parser can handle the following doc types: {str(file_types)}"
