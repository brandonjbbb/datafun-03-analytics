"""
Brandon's Analytics Project
This script fetches, processes, and writes data from the web.
"""

# Standard library imports
import csv
import pathlib
import ssl

# External library imports
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import ssl_


class SSLAdapter(HTTPAdapter):
    """An adapter that allows the use of a custom SSL context."""

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs["ssl_context"] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)


def fetch_and_write_txt_data(folder_name, filename, url):
    """
    Fetch data from a URL and save it as a text file.

    Args:
        folder_name (str): The name of the folder to save the file in.
        filename (str): The name of the file to save the data as.
        url (str): The URL to fetch data from.
    """
    try:
        # Create a custom SSL context that allows weak DH key sizes
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers("DEFAULT:@SECLEVEL=1")

        # Bypass SSL verification and attach custom SSL context to requests session
        session = requests.Session()
        adapter = SSLAdapter(ssl_context=ssl_context)
        session.mount("https://", adapter)

        response = session.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors

        if response.status_code == 200:
            file_path = pathlib.Path(folder_name).joinpath(filename)
            file_path.parent.mkdir(
                parents=True, exist_ok=True
            )  # Create folder if it doesn't exist
            with file_path.open("w") as file:
                file.write(response.text)
            print(f"Data saved to {file_path}")
        else:
            print(f"Failed to fetch data: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def process_txt_file(folder_name, filename, output_filename):
    """
    Process the text file to analyze content and save the results.

    Args:
        folder_name (str): The name of the folder containing the file.
        filename (str): The name of the file to process.
        output_filename (str): The name of the file to save the processed results.
    """
    file_path = pathlib.Path(folder_name).joinpath(filename)
    output_path = pathlib.Path(folder_name).joinpath(output_filename)

    # Check if the file exists before processing
    if not file_path.exists():
        print(
            f"The file {file_path} does not exist. Please ensure data fetching is successful."
        )
        return

    try:
        # Read the file content
        with file_path.open("r") as file:
            content = file.read()

        # Analyze the content (e.g., count words)
        word_count = len(content.split())
        unique_words = set(content.split())
        unique_word_count = len(unique_words)

        # Write the analysis results to an output file
        with output_path.open("w") as output_file:
            output_file.write(f"Word Count: {word_count}\n")
            output_file.write(f"Unique Word Count: {unique_word_count}\n")
            output_file.write(f"Unique Words: {', '.join(unique_words)}\n")

        print(f"Processed data saved to {output_path}")

    except Exception as e:
        print(f"An error occurred while processing the file: {e}")


def main():
    """Main function to demonstrate fetching, saving, and processing data."""
    txt_folder_name = "data-txt"
    txt_filename = "data.txt"
    txt_url = "https://shakespeare.mit.edu/romeo_juliet/full.html"
    output_filename = "results.txt"

    # Fetch and save the data
    fetch_and_write_txt_data(txt_folder_name, txt_filename, txt_url)

    # Process the saved text file
    process_txt_file(txt_folder_name, txt_filename, output_filename)


if __name__ == "__main__":
    main()
