import os
import tqdm
import click
import requests
import logging
from imagespuller import ImageSearch
from colorama import Fore, Style
from mimetypes import guess_extension

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--query", "-q", help="Query for image on search engine")
@click.option("--search-engine", "-s", default="google", help="Search Engine to find (default: google)")
@click.option("--dist", "-d", default="images", help="Destination folder to save images (default: downloaded_images)")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging")
def function_exec(query, search_engine, dist, verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    if query:
        search = ImageSearch()

        if search_engine == "google" or search_engine == "yandex":
            try:
                session = requests.Session()
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
                session.headers.update(headers)

                images = search.search_images(query, provider=search_engine, max_pages=1)
                
                if images:
                    logger.info(f"Found {len(images)} images for '{query}' on {search_engine}. Downloading...")
                    for i, image_url in enumerate(tqdm.tqdm(images, desc="Downloading", unit="image")):
                        try:
                            response = session.get(image_url)
                            if response.status_code == 200:
                                # Guess the file extension if it's not provided in the URL
                                file_extension = os.path.splitext(str(image_url).split("/")[-1])[-1]
                                if not file_extension:
                                    file_extension = guess_extension(response.headers.get('content-type', ''))
                                    if file_extension:
                                        file_extension = "." + file_extension.split("/")[-1]
                                    else:
                                        file_extension = ".jpg"  # Default to .jpg if extension cannot be guessed
                                filename = f"{os.urandom(35).hex()}{file_extension}"
                                filepath = os.path.join(dist, filename)
                                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                                with open(filepath, 'wb') as f:
                                    f.write(response.content)
                        except Exception as e:
                            logger.error(f"Error downloading image: {str(e)}")
                    logger.info("Download completed successfully.")
                else:
                    logger.warning(f"No images found for '{query}' on {search_engine}.")
            except Exception as e:
                logger.error(f"An error occurred: {str(e)}")
        else:
            logger.error("Invalid search engine. Please choose 'google' or 'yandex'.")
    else:
        logger.error("Query is required.")

if __name__ == "__main__":
    function_exec()
