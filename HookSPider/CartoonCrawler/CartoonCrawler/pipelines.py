# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import copy

import logging
logger = logging.getLogger('mangabz_logger')

class CartooncrawlerPipeline(object):

    def open_spider(self, spider):
        self.file = open('./spiders/imgs.csv', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        lst_values = [str(i) for i in item.values()]
        line = ','.join(lst_values) + ';\n'
        self.file.write(line)
        return item


class ImgspiderPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        image_url = item['image_url']
        yield Request(image_url)

    def file_path(self, request, response=None, info=None, *, item):
    # #     # 该方法是在图片将要被存储的时候调用，来获取这个图片存储路径
        mid = item['mid']
        cid = item['cid']
        title = item['title']
        # 每一章的图片下载顺序
        cindex = item['cindex']
        one_seq = item['one_seq']
        full_path = '{}/{}_{}/{}.jpg'.format(mid, cid, title, one_seq)
    # #     # logger.info(full_path)
        return full_path	# 返回文件名

    def item_completed(self, results, item, info):
        # logger.info(results)
        path = [s['path'] for ok, s in results if ok]
        url =  [s['url'] for ok, s in results if ok]
        item['img_path'] = path
        item['img_url'] = url
        # logger.info(item)
        return item # 返回给下一个即将被执行的管道类