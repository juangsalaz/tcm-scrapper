import scrapy
import csv


class ScholarShipsHome(scrapy.Spider):
    name = "ScholarShipsHome"

    def start_requests(self):
        url = 'https://www.unigo.com/scholarships' 
        yield scrapy.Request(url=url, callback=self.parse, meta = {"url": url})

    def parse(self, response):
        list_object = response.xpath("//div[@class='page-content']")
        data_list = []
        
        for cards in list_object.xpath(".//div[contains(@class, 'scholarship-directory-group-container')]"):
            data = {}
            data["Title"] = cards.xpath(".//h3[@class='scholarship-group-category-title']/a/text()").get()
            if data["Title"] != None:
                data["Request Url"] = response.meta['url']
                data["Next Url"] = cards.xpath(".//h3[@class='scholarship-group-category-title']/a/@href").get()
                data["Description"] = cards.xpath(".//div[contains(@class, 'scholarship-group-info')]/p/text()").get()
                data["Award Text"] = cards.xpath(".//span[@class='scholarship_group_info_data-title']/text()").get()
                if data["Award Text"] != None:
                    data["Award Text"] = cards.xpath(".//span[@class='scholarship_group_info_data-title']/text()")[0].getall()
                    data["Award Money"] = cards.xpath(".//span[@class='scholarship_group_info_data-title']/text()")[1].getall()
                    data["Total Text"] = cards.xpath(".//span[@class='scholarship_group_info_data']/text()")[0].getall()
                    data["Total Money Text"] = cards.xpath(".//span[@class='scholarship_group_info_data']/text()")[1].getall()
                data["Url Link Button"] = cards.xpath(".//div[contains(@class, 'scholarship-group-link')]/a/@href").get()
                data["Image Url"] = cards.xpath(".//div[contains(@class, 'scholarship-group-image')]/img/@src").get()
                data_list.append(data)
        rows = ["Title", "Next Url", "Description", "Award Text", "Award Money", "Total Text", "Total Money Text", "Url Link Button","Image Url", "Request Url"]
        with open("homepagedata.csv", 'w+') as f:
            writer_ob = csv.DictWriter(f, rows)
            writer_ob.writeheader()
            writer_ob.writerows(data_list)