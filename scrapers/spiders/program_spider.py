import scrapy
from scrapy.selector import Selector
import time
from components.logger import Logger
from components.helper import error_message, driver_file
from components.database import Database
from selenium import webdriver
import re


class ProgramSpider(scrapy.Spider):
    allowed_domains = ['www.zcu.cz']
    name = "program_spider"
    start_urls = ["https://www.zcu.cz/cs/Admission/Study-fields/index.html"]

    def __init__(self):
        super().__init__()
        self.database = Database()
        self.logging = Logger(spider=self.name).logger
        self.driver = webdriver.Chrome(driver_file())
        self.programs = []

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logging.info('Visiting ' + response.url)
        self.driver.get(response.url)
        try:
            time.sleep(1)
            program_wrapper = self.driver.find_element_by_css_selector('div.article-item')
            selector = Selector(text=program_wrapper.get_attribute('innerHTML'))
            self.extract_programs(selector)
            first_item = self.programs[0]
            self.item_index = 1
            self.parse_detail(first_item)
        except Exception as e:
            self.logging.error("Error getting body" + error_message(e))

    def parse_detail(self, item):
        try:
            if self.test_url(item["url"]):
                self.process_program(item)
        except Exception as e:
            self.logging.error("Error getting body" + error_message(e))
        finally:
            if (self.item_index < len(self.programs)):
                self.current_item = self.programs[self.item_index]
                self.item_index += 1
                self.parse_detail(self.current_item)

    def test_url(self, url):
        return re.match("https:\/\/www.zcu.cz\/cs\/Admission\/Study-fields\/index.html\?.*", url)

    def extract_programs(self, selector):
        programs = selector.css("li.typo-base-small")
        for program in programs:
            link = program.css("a.head-bold-active::attr(href)").extract_first()
            name = program.css("a.head-bold-active::text").extract_first()
            faculty = program.css("div.faculty-tag::text").extract_first()
            url = "https://www.zcu.cz" + link
            item = {"url": url, "name": name, "faculty": faculty}
            self.programs.append(item)

    def process_program(self, item):
        self.logging.info('Visiting program URL ' + item["url"])
        self.driver.get(item["url"])
        try:
            time.sleep(1)
            body = self.driver.find_element_by_css_selector('body')
            selector = Selector(text=body.get_attribute('innerHTML'))
            item["catalogue_url"] = selector.css("a#detailButton::attr(href)").extract_first()
            """
            content = selector.css("div.content")
            texts = content.css("p::attr(text)").extract()
            print(texts)
            item["description"] = texts[0]
            item["learning"] = texts[1]
            item["practical"] = texts[2]
            """
            print(item)
            self.database.insert_program(item)
        except Exception as e:
            self.logging.error("Error getting body" + error_message(e))
