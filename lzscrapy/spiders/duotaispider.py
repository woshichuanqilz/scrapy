# -*- coding: utf-8 -*-
import scrapy

class LoginSpider(scrapy.Spider):
    name = 'example.com'
    start_urls = ['https://duotai.org/login']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'email': '513278236@qq.com', 'password': 'woshichuanqilz72'},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return
        print(response.body)

        # continue scraping with authenticated session...
