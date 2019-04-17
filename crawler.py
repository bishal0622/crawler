import scrapy
import json
import csv


class AuthorSpider(scrapy.Spider):
    name = 'Links'

    start_urls = ['https://www.healwithfood.org/colorectalcancer/foods.php',
                  'https://www.healwithfood.org/constipation/foods.php',
                  'https://www.healwithfood.org/constipation/foods2.php',
                  'https://www.healwithfood.org/hemorrhoids/foods.php']
    images_data = {}

    def parse(self, response):
        for img in response.css('h2::text'):
            yield response.follow(img, self.parse_images)

    def parse_images(self, response):
        def extract_with_css_h2(query):
            query_response = response.css(query).extract()
            temp = []
            for x in query_response:
                temp.append(x.split("\xa0")[1].replace('\r\n', '').lower())
            return temp

        def extract_with_css_h1(query):
            disease = ['cancer', 'constipation']
            query_response = response.css(query).extract()[0].lower()
            for i in disease:
                if i in query_response:
                    return i
                else:
                    query_response

        yield {
            'disease': extract_with_css_h1('h1::text'),
            'food': extract_with_css_h2('h2::text')
        }


with open('output.json') as json_file:
    data = json.load(json_file)
    print(data)
    f = csv.writer(open("test.csv", "w"))

    # Write CSV Header, If you dont need that, remove this line
    f.writerow(["pk", "model", "codename", "name", "content_type"])

    # for x in data:
    #     f.writerow([x["medicine"],
    #                 x["foods"]])
