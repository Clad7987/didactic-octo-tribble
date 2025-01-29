import scrapy

from urllib.parse import urlparse

class FapdungeonSpider(scrapy.Spider):
    name = "fapdungeon"
    allowed_domains = ["fapdungeon.com"]
    start_urls = []

    def __init__(self, start_url=None, *args, **kwargs):
        super(FapdungeonSpider, self).__init__(*args,**kwargs)
        self.start_urls = [start_url] if not isinstance(start_url, list) else start_url

    def parse(self, response):
        article = response.xpath(".//article[contains(@id, 'post-')]")

        path_segments = urlparse(response.url).path.strip("/").split("/")

        item =  {
            "videos": article.xpath(".//source/@src").getall(),
            "images": article.xpath(".//img/@src").getall(),
            "folder": path_segments[1]
        }

        yield item

        page_links = response.xpath("//div[contains(@class,'page-links')]")
        next_page = page_links.xpath(".//a[contains(@class,'post-page-numbers')]")
        curr_page = page_links.xpath("//span[contains(@class,'current')]/span/text()")

        if next_page:
            for np in next_page:
                if int(np.xpath(".//span/text()").get()) < int(curr_page.get()):
                    next_page.pop(next_page.index(np))
            yield response.follow(next_page[0].attrib['href'], self.parse)
