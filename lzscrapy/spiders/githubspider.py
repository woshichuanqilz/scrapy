#!/usr/bin/env python
# -*- coding:utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest


class GitHubLogin(scrapy.Spider) :
    name = "GH"
    allowed_domains = ["github.com"]
    start_urls = [
        "http://github.com"
    ]

    #重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
    def start_requests(self):
        return [Request("https://github.com/login", meta = {'cookiejar' : 1}, callback = self.post_login)]

    #FormRequeset出问题了
    def post_login(self, response):
        print 'Preparing login'
        authenticity_token = Selector(response).xpath("/html/body/div[4]/div[1]/div/form/div[1]/input[2]/@value").extract()[0]

        #FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        #登陆成功后, 会调用after_login回调函数
        formdata_utf = u"\u2713".encode('utf-8')
        return [FormRequest.from_response(response,   #"http://www.zhihu.com/login",
                            meta = {'cookiejar' : response.meta['cookiejar']},
                            formdata = {
                            'authenticity_token': authenticity_token,
                            'commit': 'Sign in',
                            'login': '513278236@qq.com',
                            'password': 'woshichuanqilz72',
                            'utf': formdata_utf
                            },
                            callback = self.after_login,
                            dont_filter = True
                            )]
 
    def after_login(self, response) :
        return [Request("https://github.com/stars", meta = {'cookiejar' : response.meta['cookiejar']}, callback = self.post_login2)]

    def post_login2(self, response):
        print "the response url is " + response.body
