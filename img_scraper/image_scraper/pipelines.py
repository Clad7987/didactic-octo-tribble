# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import scrapy
import requests
import logging

from uuid import uuid4
from urllib.parse import urlparse

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class ImageScraperPipeline(ImagesPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = requests.Session()
        self.item_filter = True

    def process_item(self, item, spider):
        image_store = spider.settings.get("IMAGES_STORE")
        folder = item.get("folder")
        items = (*item.get("images"), *item.get("videos")) if not self.item_filter else item.get("images")
        for i in items:
            image_name = self.extract_file_name(i)

            album_path = os.path.join(image_store, folder)
            os.makedirs(album_path, exist_ok=True)

            response = self.session.get(i, stream=True)
            if response.status_code == 200:
                image_name = f"{uuid4()}-{image_name}"
                image_path = os.path.join(album_path, image_name)

                with open(image_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
        return item

    @staticmethod
    def extract_file_name(url):
        path_segments = urlparse(url).path.strip("/").split("/")
        if len(path_segments) >= 2:
            return path_segments[-1]
        return "default"

    def close_spider(self, spider):
        self.session.close()
