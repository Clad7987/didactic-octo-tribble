from scrapy.crawler import CrawlerProcess
#from scrapy.utils.project import get_project_settings
import json
# Importe seu spider
from image_scraper.spiders.fapdungeon import FapdungeonSpider
import os
import tqdm

def get_project_settings():
    settings = {}
    settings_path = os.path.join(os.path.dirname(__file__), "image_scraper", "settings.py")
    with open(settings_path, "r") as file:
        for line in file.readlines():
            if line.startswith("#") or len(line) < 2:
                continue
            key, value = line.split("=")
            settings.update({key.strip(): eval(value.strip())})

    settings['IMAGES_STORE'] = os.path.join(os.path.dirname(__file__), "image_scraper", "Downloads")
    settings['FILES_STORE'] = os.path.join(os.path.dirname(__file__), "image_scraper", "Downloads")
    settings['LOG_ENABLED'] = False
    return settings


def main():
    # Carregue as configurações do Scrapy
    process = CrawlerProcess(get_project_settings())
    #process = CrawlerProcess(get_project_settings())

    url_path = os.path.join(os.path.dirname(__file__), "urls.txt")
    with open(url_path) as file:
        urls = [item.strip() for item in file.readlines() if item.startswith("http")]

    with tqdm.tqdm(total=len(urls), desc="Downloading URLs", unit="url") as bar:
        for url in urls:
            process.crawl(FapdungeonSpider, start_url=url)
            bar.update(1)

    process.start()

if __name__ == '__main__':
    main()
