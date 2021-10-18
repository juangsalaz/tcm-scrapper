import scrapy
import csv


class ScholarShipCategoryHome(scrapy.Spider):
    name = "ScholarShipCategoryHome"

    def start_requests(self):
        with open('homepagedata.csv', 'r') as file_csv:
            csv_reader = csv.DictReader(file_csv)
            for row in csv_reader:
                filename = row["Next Url"].split('/')[-1]
                yield scrapy.Request(url=row["Next Url"], callback=self.parse, meta = {'filename': filename , 'url':row["Next Url"]})

    def write_in_text_file(self, url):
        with open("NoNextUrlCard.txt", 'a+') as f:
            f.write(url + "\n")

    def parse(self, response):
        list_object = response.xpath("//div[@id='scholarshipWrap']")
        data_list = []
        if list_object.get() == None:
            self.write_in_text_file(response.meta["url"])
        
        for cards in list_object.xpath(".//div[contains(@class, 'scholarshipBrief')]"):
            data = {}
            data["Title"] = cards.xpath(".//h3/a/text()").get()
            if data["Title"] != None:
                data["Request Url"] = response.meta["url"]
                data["Next Url"] = cards.xpath(".//h3/a/@href").get()
                data["Description"] = cards.xpath(".//p/text()").get()
                data["Award Text"] = cards.xpath(".//div[@class='totalAvail']/p/span/text()").get()
                data["Award Money"] = cards.xpath(".//div[@class='totalAvail']/p/text()").get()
                data["Total Text"] = cards.xpath(".//div[@class='totalValue']/p/span[@class='text']/text()").get()
                data["Total Money Text"] = cards.xpath(".//div[@class='totalValue']/p/text()").get()
                data["Url Link Button"] = cards.xpath(".//div[contains(@class, 'scholarship_directory_link_container')]/a/@href").get()
                data["Image Url"] = cards.xpath(".//div[contains(@class, 'scholarship_directory_image_container')]/img/@src").get()
                data_list.append(data)
        rows = ["Request Url", "Title", "Next Url", "Description", "Award Text", "Award Money", "Total Text", "Total Money Text", "Url Link Button","Image Url"]
        filename_ = '001Category' + response.meta['filename'] +'.csv'
        with open(filename_, 'a+') as f:
            writer_ob = csv.DictWriter(f, rows)
            writer_ob.writeheader()
            writer_ob.writerows(data_list)