import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from ..items import CarscrapperItem

class CarsSpider(scrapy.Spider):
    name = "cars"
    page_number = 2
    start_urls = ['https://ab.onliner.by/bmw']

    def __init__(self):
        options = Options()
        options.headless = True 
        self.driver = webdriver.Firefox(options=options)
    
    def parse(self, response):
        item = CarscrapperItem()
        
        self.driver.get(response.url)
        res = response.replace(body=self.driver.page_source)

        for car_div in res.css('.vehicle-form__offers-unit'):
            name = car_div.css('.vehicle-form__link_noreflex::text').extract_first()
            price = car_div.css('.vehicle-form__offers-part.vehicle-form__offers-part_price').css('.vehicle-form__description_condensed-other::text').extract_first()
            img = car_div.css('.vehicle-form__image::attr(style)').extract_first()
            
            item['name'] = name
            item['price'] = price
            item['img'] = img

            yield item

        next_page = 'https://ab.onliner.by/bmw?page=' + str(CarsSpider.page_number)
        if CarsSpider.page_number <= 45:
            CarsSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

        