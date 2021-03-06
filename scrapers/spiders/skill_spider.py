import scrapy
from scrapy.selector import Selector
import time
from components.logger import Logger
from components.helper import error_message, driver_file
from components.database import Database
from selenium import webdriver
import re


row_headers = [
    "Odborné znalosti - pro úspěšné zvládnutí oboru se předpokládá, že je student před zahájením výuky schopen:",
    "Odborné dovednosti - pro úspěšné zvládnutí oboru se předpokládá, že student před zahájením výuky dokáže:",
    "Obecné způsobilosti - před zahájením studia oboru je student schopen:",
    "Odborné znalosti - po absolvování oboru prokazuje student znalosti:",
    "Odborné dovednosti - po absolvování oboru prokazuje student dovednosti:",
    "Obecné způsobilosti - po absolvování oboru je student schopen:",
    "Odborné znalosti - pro dosažení odborných znalostí jsou užívány vyučovací metody:",
    "Odborné dovednosti - pro dosažení odborných dovedností jsou užívány vyučovací metody:",
    "Obecné způsobilosti - pro dosažení obecných způsobilostí jsou užívány vyučovací metody:",
    "Odborné znalosti - odborné znalosti dosažené studiem oboru jsou ověřovány hodnoticími metodami:",
    "Odborné dovednosti - odborné dovednosti dosažené studiem oboru jsou ověřovány hodnoticími metodami:",
    "Obecné způsobilosti - obecné způsobilosti dosažené studiem oboru jsou ověřovány hodnoticími metodami:"
]

skip_rows = [
    "Předpoklady",
    "Výsledky učení",
    "Vyučovací metody",
    "Hodnoticí metody"
]

class SkillSpider(scrapy.Spider):
    allowed_domains = ['portal.zcu.cz']
    name = "skill_spider"
    start_urls = ["https://portal.zcu.cz"]

    def __init__(self):
        super().__init__()
        self.database = Database()
        self.logging = Logger(spider=self.name).logger
        self.driver = webdriver.Chrome(driver_file())
        self.url_index = 0
        self.program_urls = self.database.get_program_urls()

    def start_requests(self):
        self.logging.info(f"Link number: {self.url_index}")
        if (self.url_index < len(self.program_urls)):
            self.current_url = self.program_urls[self.url_index]
            self.url_index += 1
            yield scrapy.Request(url=self.current_url, callback=self.parse, dont_filter=True)


    def test_program_url(self, url):
        return re.match("https:\/\/portal.zcu.cz*", url)

    def parse(self, response):
        self.logging.info('Visiting ' + response.url)
        self.driver.get(response.url)
        try:
            time.sleep(1)
            body = self.driver.find_element_by_css_selector('body')
            selector = Selector(text=body.get_attribute('innerHTML'))
            self.extract_table(selector)
            self.extract_program_header(selector)
        except Exception as e:
            self.logging.error("Error getting body" + error_message(e))
        finally:
            self.logging.info(f"Link number: {self.url_index}")
            if (self.url_index < len(self.program_urls)):
                self.current_url = self.program_urls[self.url_index]
                self.url_index += 1
                yield scrapy.Request(url=self.current_url, callback=self.parse, dont_filter=True)



    def extract_program_header(self, selector):
        item = {}
        table = selector.xpath('///*[@id="prohlizeniEntitaSubdetailPanesCoat"]/table[0]/tbody')
        item["specialization_name"] = table.xpath('tr[0]/td[0]').extract_first()
        item["specialization_number"] = selector.xpath('tr[2]/td[1]').extract_first()
        item["shortcut"] = selector.xpath('tr[1]/td[0]').extract_first()
        item["form"] = selector.xpath('tr[3]/td[0]').extract_first()
        item["type"] = selector.xpath('tr[3]/td[1]').extract_first()
        item["length"] = selector.xpath('tr[4]/td[0]').extract_first()
        item["goal"] = selector.xpath('tr[6]/td[0]').extract_first()
        item["annotation"] = selector.xpath('tr[7]/td[0]').extract_first()
        print(item)
        #self.database.insert_program(item)

    def extract_table(self, selector):
        table = selector.css("div.prohlizeniEntitaSubdetailPanesCoat").css("table")
        rows = table.css("td::text").extract()
        self.parse_table(rows)

    def parse_table(self, rows):
        for row in rows:
            if row in row_headers:
                item["skill_type"] = self.get_skill_type(row)
                item["type"] = self.get_type(row)
            else:
                item["name"] = row
                self.database.insert_skill(item)


    def get_skill_type(self, row):
        if "Odborné znalosti" in row:
            return "znalosti"
        if "Odborné dovednosti" in row:
            return "dovednosti"
        if "Obecné způsobilosti" in row:
            return "způsobilosti"

    def get_type(self, row):
        if "před zahájením" in row:
            return "před"
        if "po absolvování" in row:
            return "po"
        if "vyučovací metody" in row:
            return "vyučovací metody"
        if "hodnoticími metodami" in row:
            return "hodnoticí metody"

