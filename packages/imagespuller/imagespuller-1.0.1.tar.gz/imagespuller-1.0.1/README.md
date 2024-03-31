# ImagesPuller

ImagesPuller is a tool for downloading images from the internet. It scrapes web data from various sources to gather image URLs and allows you to download them to your local machine.

`imagespuller` is a tool designed to fetch images from various sources across the internet, allowing you to create your own datasets for various purposes, such as machine learning, data analysis, or simply gathering reference images.

## Features

- Supports scraping image URLs from multiple search engines.
- Easy-to-use interface.
- Ability to specify the search query and number of pages to scrape.
- Flexible output directory configuration.

## Installation

You can install `imagespuller` using pip:

```bash
pip install imagespuller
```

## Cli

```
Usage: python -m imagespuller [OPTIONS]

Options:
  -q, --query TEXT          Query for image on search engine
  -s, --search-engine TEXT  Search Engine to find (default: google)
  -d, --dist TEXT           Destination folder to save images (default:
                            downloaded_images)
  -v, --verbose             Enable verbose logging
  --help                    Show this message and exit.
```

```
imagespuller -q Cat
```


## Usage


```python
from imagespuller import ImageSearch

searcher = ImageSearch()

image_urls = searcher.search_images("cat", provider="google", max_pages=1)

searcher.save_images(image_urls, query="cats", dist_folder="downloaded_images")
```

## Supported Providers

- Google
- Yandex

You can specify the provider when searching for images. By default, Google is used.

## Copyright Risks

Downloading and using images from the internet may pose copyright risks. Users of ImagesPuller are responsible for ensuring that they have the appropriate rights or permissions to use the downloaded images for their intended purposes. It is recommended to review the terms of use and licensing agreements of the sources from which images are downloaded to avoid copyright infringement.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
