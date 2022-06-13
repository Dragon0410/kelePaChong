import scrapy
from scrapy import Request
from ..items import XiaoshuoItem

class ZonghengSpider(scrapy.Spider):
    name = 'zongheng'
    allowed_domains = ['zongheng.com']
    start_urls = []
    for p in range(1, 20):
        url_page = f"http://book.zongheng.com/store/c0/c0/b0/u0/p{p}/v9/s9/t0/u0/i1/ALL.html"
        start_urls.append(url_page)

    def parse(self, response):
        books = response.xpath('//div[@class="store_collist"]/div[@class="bookbox fl"]/div[@class="bookinfo"]/div[@class="bookname"]/a/@href').extract()
        for url in books:
            yield Request(url, callback=self.bookinfo_parse)

    def bookinfo_parse(self, response):
        book_name_link = response.url
        selector = response.xpath('//div[@class="book-info"]')
        book_name = selector.xpath('//div[@class="book-name"]//text()').extract()
        book_author = response.xpath('//div[@class="book-author"]/div[@class="au-name"]/a/text()').extract()
        book_author_link = response.xpath('//div[@class="book-author"]/div[@class="au-name"]/a/@href').extract()
        edit_status = selector.xpath('//div[@class="book-label"]/a[1]//text()').extract()
        book_category = selector.xpath('//div[@class="book-label"]/a[2]//text()').extract()
        book_tags = selector.xpath('//div[@class="book-label"]/span/a//text()').extract()
        book_total_words = selector.xpath('//div[@class="nums"]/span[1]/i//text()').extract()
        book_count_recommends = selector.xpath('//div[@class="nums"]/span[2]/i//text()').extract()
        book_total_clicks = selector.xpath('//div[@class="nums"]/span[3]/i//text()').extract()
        book_summary = selector.xpath('//div[@class="book-dec Jbook-dec hide"]/p//text()').extract()
        book_catalogue_link = selector.xpath('//div[@class="btn-group"]//a[@class="all-catalog"]/@href').extract()

        # 如果没有找到相应的数据，该字段为 "" 或 0
        book_name = ''.join(book_name).strip() if book_name else ''
        book_author = ''.join(book_author) if book_author else ''
        book_author_link = ''.join(book_author_link) if book_author_link else ''
        edit_status = ''.join(edit_status) if edit_status else ''
        book_category = ''.join(book_category) if book_category else ''
        book_tags = ','.join(book_tags) if book_tags else ''
        book_total_words = int(float(''.join(book_total_words).strip().replace('万','')) * 10000) if book_total_words else 0
        book_count_recommends = int(float(''.join(book_count_recommends).strip().replace('万','')) * 10000) if book_count_recommends else 0
        book_total_clicks = int(float(''.join(book_total_clicks).strip().replace('万','')) * 10000) if book_total_clicks else 0
        book_summary = ''.join(book_summary).replace(' ','').replace('\u3000', '').replace('\r\n', '').replace('\xa0', '') if book_summary else ''
        book_catalogue_link = ''.join(book_catalogue_link) if book_catalogue_link else ''
        
        item = XiaoshuoItem()
        item['book_name'] = book_name
        item['book_author'] = book_author
        item['book_author_link'] = book_author_link
        item['book_name_link'] = book_name_link
        item['edit_status'] = edit_status
        item['book_category'] = book_category
        item['book_tags'] = book_tags
        item['book_total_words'] = book_total_words
        item['book_count_recommends'] = book_count_recommends
        item['book_total_clicks'] = book_total_clicks
        item['book_summary'] = book_summary
        item['book_catalogue_link'] = book_catalogue_link
        yield item