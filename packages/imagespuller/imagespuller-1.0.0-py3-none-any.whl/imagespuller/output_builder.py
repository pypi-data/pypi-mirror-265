import os
import requests

class OutputBuilder:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def save_images(self, image_urls: list, query: str):
        query_folder = os.path.join(self.output_dir, query)
        if not os.path.exists(query_folder):
            os.makedirs(query_folder)

        for i, url in enumerate(image_urls):
            filename = os.path.join(query_folder, f"{i}.jpg")
            with open(filename, 'wb') as f:
                try:
                    response = requests.get(url)
                    f.write(response.content)
                except Exception as e:
                    print(f"Failed to download {url}: {e}")
