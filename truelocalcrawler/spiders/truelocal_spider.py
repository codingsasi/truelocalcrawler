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
            while(pager < 50 and pager > 0):
                next_url = safe_url + str(pager) +'/'
                header = requests.head(next_url)
                if header.status_code != 404:
                    print next_url
                    print "==============------------------=================-=-------"
                    start_urls.append(next_url)
                    pager = pager + 1
                    if pager % 20 == 0:
                        time.sleep(10)
                else:
                    print next_url
                    print "4040440404040404"
                    pager = 0

    def parse(self, response):
        print response
        print "======================--------------------==================="
        companies = []
        for search_result in response.css("div.search-result"):
            company = Company()
            company['name'] = search_result.css("span.name > a::text").extract_first()
            company['phone'] = search_result.css("span.tl-phone-show a#TolHalfPhoneHrefId::attr(href)").extract_first()
            company['address'] = search_result.css("div.service-and-address span.address.secondary::text").extract_first()
            company['category'] = response.css("div.breadcrumb-container ul li > span::text").extract_first()
            company['link'] = ""
            companies.append(company)

        return companies



        """yield scrapy.Request(url, callback=self.parse_links, meta={
            'splash': {
               'endpoint': 'render.html',
               'args': {'wait': 0.5}
               }
            })"""


    def parse_links(self, response):
        print response
        print "========-=-=-=-======================="
        selector = Selector(response)
        details = selector.css("div.text-holder")
        company = Company()
        company['name'] = details.css("h1::text").extract_first()
        company['phone'] = details.css("div#phone-1 span.phone::text").extract_first()
        address = []
        line = details.css("div#phone-1 div.contact-holder span#address p > span > span::text").extract_first()
        address.append(line)
        line = details.css("div#phone-1 div.contact-holder span#address p")[1]
        for word in line.css("span"):
            address.append(word.css("::text").extract_first())
        company['address'] = " ".join(address)
        company['link'] = ''
        company['category'] = details.css(".title #categories-area > h4 > div::text").extract_first()
        print "======================================="
        print company['name']
        print company['phone']
        print company['category']
        print "======================================="
        return company
