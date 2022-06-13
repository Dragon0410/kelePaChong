# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


class XiaoshuoPipeline:

    def process_item(self, item, spider):
        return item


class Xiaoshuo_csv_Pipline:

    def __init__(self):
        self.csv_hander = open("./xiaoshuo.csv",
                               'a',
                               newline='',
                               encoding='utf-8')
        fields = [
            'book_name', 'book_author', 'book_author_link', 'book_name_link',
            'edit_status', 'book_category', 'book_tags', 'book_total_words',
            'book_count_recommends', 'book_total_clicks', 'book_summary',
            'book_catalogue_link'
        ]
        self.csv_write = csv.DictWriter(self.csv_hander, fieldnames=fields)
        self.csv_write.writeheader()

    def process_item(self, item, spider):
        self.csv_write.writerow(item)

    def close_item(self, spider):
        self.csv_hander.close()