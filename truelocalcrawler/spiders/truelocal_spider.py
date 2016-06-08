import scrapy, os
import requests
import time
from truelocalcrawler.items import Company
from scrapy_splash import SplashRequest
from scrapy.selector import Selector

class TrulocalCompanySpider(scrapy.Spider):
    name = 'truelocal'
    allowed_domains = ['www.truelocal.com.au']

    start_urls = []
    with open(os.getcwd() + '/start_urls.csv') as f:
        for url in f.readlines():
            safe_url = url.rstrip()
            start_urls.append(safe_url)
            pager = 2
            while(pager):
                next_url = safe_url + str(pager) +'/'
                header = requests.head(next_url)
                if header.status_code != 404:
                    start_urls.append(next_url)
                    pager = pager + 1
                    if pager % 20 == 0:
                        time.sleep(10)
                else:
                    pager = 0

    def parse(self, response):
        for href in response.css("ul#search li span.name a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_links, meta={
                'splash': {
                   'endpoint': 'render.html',
                   'args': {'wait': 0.5}
                   }
                })


    def parse_links(self, response):
        print response
        print "========-=-=-=-======================="
        selector = Selector(response)
        details = selector.css("div.text-holder")
        company = Company()
        company['name'] = details.css("h1::text").extract_first()
        company['phone'] = details.css("div#phone-1 span.phone::text").extract_first()
        address = []
        line = details.css("div#phone-1 div.contact-holder span#address p > span::text").extract_first()
        address.append(line)
        line = details.css("div#phone-1 div.contact-holder span#address p")[1]
        for word in line.css("span"):
            address.append(word.css("::text").extract_first())
        company['address'] = " ".join(address)
        company['link'] = ''
        company['category'] = details.css("span.title a::text").extract_first()
        print "======================================="
        print company['name']
        print company['phone']
        print company['category']
        print "======================================="
        return company
