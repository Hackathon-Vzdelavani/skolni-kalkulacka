import scrapy
from scrapy.selector import Selector
import time
from components.logger import Logger
from components.helper import error_message, driver_file
from components.sqlite import SqliteDatabase
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
    allowed_domains = ['www.zcu.cz']
    name = "skill_spider"
    start_urls = ["https://portal.zcu.cz/StagPortletsJSR168/CleanUrl?urlid=prohlizeni-browser-obor&browserFakulta=FDU&browserProgram=1808&browserObor=4036&browserRok=2021"]

    def __init__(self):
        super().__init__()
        self.database = SqliteDatabase()
        self.logging = Logger(spider=self.name).logger
        self.driver = webdriver.Chrome(driver_file())
        self.url_index = 0
        self.program_urls = self.database.get_programs()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

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
        except Exception as e:
            self.logging.error("Error getting body" + error_message(e))
        finally:
            self.logging.info(f"Link number: {self.url_index}")
            if (self.url_index < len(self.program_urls)):
                self.current_url = self.program_urls[self.url_index]
                self.url_index += 1
                yield scrapy.Request(url=self.current_url, callback=self.parse)

    def extract_table(self, selector):
        table = selector.css("div.prohlizeniEntitaSubdetailPanesCoat").css("table")
        rows = table.css("td::text").extract()
        self.parse_table(rows)

    def parse_table(self, rows):
        skill_type, type = None, None
        for row in rows:
            if row in row_headers:
                skill_type = self.get_skill_type(row)
                type = self.get_type(row)
            else:
                self.database.


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

