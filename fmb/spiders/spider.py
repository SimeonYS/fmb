import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import FmbItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class FmbSpider(scrapy.Spider):
	name = 'fmb'
	start_urls = ['https://www.fmb.com/news-and-community/press-releases']

	def parse(self, response):
		post_links = response.xpath('//li[@class="featured"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="date"]/p/strong/text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//article/div[2]//text()[not (ancestor::center)]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=FmbItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
