# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter, is_item
from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import DropItem


from PchomeCrawler.items import PchomecrawlerItem
from PchomeCrawler.items import PchomecQtyItem

class PchomecrawlerPipeline(object):
    def __init__(self):
        self.ids_seen = set()
        self.file = open('test.csv', 'ab+')
        self.exporter = CsvItemExporter(self.file , join_multivalued='+', encoding='utf-8', )
        self.file_qty = open('test_qty.csv', 'ab+')
        self.exporter_qty = CsvItemExporter(self.file_qty, join_multivalued='+', encoding='utf-8')

    def open_spider(self, spider):
        self.exporter.start_exporting()
        self.exporter_qty.start_exporting()

    def process_item(self, item, spider):
        if isinstance(item, PchomecrawlerItem):
            adapter = ItemAdapter(item)
            if adapter['one_item_id'] in self.ids_seen:
                self.ids_seen.add(adapter['one_item_id'])
                self.exporter.export_item(item)
                return item
                # raise DropItem("Duplicate item found: %r" % item)
            else:
                self.ids_seen.add(adapter['one_item_id'])
                self.exporter.export_item(item)
                return item
        elif isinstance(item, PchomecQtyItem):
            self.exporter_qty.export_item(item)
            return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        self.exporter_qty.finish_exporting()
        self.file_qty.close()

