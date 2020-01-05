# -*- coding: utf-8 -*-
import scrapy


class RipOffReport(scrapy.Spider):
    name = 'ripoffreport'
    allowed_domains = ['www.ripoffreport.com']
    start_urls = ['https://www.ripoffreport.com/reports/latest-reports?&pg=1']


    def parse(self, response):
        urls = response.css('.title').xpath("./a/@href").extract()
        print(urls)
        for url in urls:
            yield response.follow(url, callback=self.extract_page)
            # yield scrapy.Request("https://www.ripoffreport.com" + url, callback=self.extract_page, dont_filter=True)
        print("Going to next page..")
        next_page = response.css('ul.pagination a::attr(href)').getall()[1]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def extract_page(self, response):
        data = {}
        data['url'] = response.url
        data['phone'] = response.xpath('//*[@id="report-view"]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/div/ul/li[1]/text()').extract()
        data['reported_by'] = "".join(response.xpath('//*[@id="report-view"]/div/div[1]/div[3]/div[2]/div[1]/div/ul/li[3]/text()').extract()).strip()
        data['web'] = response.xpath('//*[@id="report-view"]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/div/ul/li[2]/a/@href').extract_first()
        data['category'] = response.xpath('//*[@id="report-view"]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/div/ul/li[3]/a/text()').extract()
        return data