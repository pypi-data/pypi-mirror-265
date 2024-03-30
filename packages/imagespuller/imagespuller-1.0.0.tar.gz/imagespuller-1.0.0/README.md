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

## Usage

```python
from imagespuller import ImageSearch, OutputBuilder

# Initialize ImageSearch and OutputBuilder
image_search = ImageSearch()
output_builder = OutputBuilder(output_dir="./downloaded_images")

# Search for images using Google
image_urls_google = image_search.search_images("cats", provider="google")

# Save images to the output directory
output_builder.save_images(image_urls_google, query="cats")
```

## Supported Providers

- Google
- Yandex

You can specify the provider when searching for images. By default, Google is used.

## Copyright Risks

Downloading and using images from the internet may pose copyright risks. Users of ImagesPuller are responsible for ensuring that they have the appropriate rights or permissions to use the downloaded images for their intended purposes. It is recommended to review the terms of use and licensing agreements of the sources from which images are downloaded to avoid copyright infringement.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
