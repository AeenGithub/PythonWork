# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PchomecrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    init_clss_id = scrapy.Field()
    init_clss_name = scrapy.Field()
    init_clss_url = scrapy.Field()
    init_clss_sort = scrapy.Field()
    init_node_id = scrapy.Field()
    init_node_name = scrapy.Field()
    init_node_url = scrapy.Field()
    init_node_sort = scrapy.Field()
    timestamp = scrapy.Field()

    one_clss_id = scrapy.Field()
    one_clss_name = scrapy.Field()
    one_clss_url = scrapy.Field()
    one_clss_sort = scrapy.Field()
    one_clss_isPick = scrapy.Field()
    one_clss_isClothing = scrapy.Field()


    second_clss_id = scrapy.Field()
    second_clss_name = scrapy.Field()
    second_clss_sort = scrapy.Field()
    second_node_id = scrapy.Field()
    second_node_name = scrapy.Field()
    second_node_sort = scrapy.Field()
    second_node_is24h = scrapy.Field()
    second_node_isVip = scrapy.Field()
    second_node_isPick = scrapy.Field()

    count_data = scrapy.Field()
    promote_count = scrapy.Field()

    total_page = scrapy.Field()
    one_page = scrapy.Field()

    one_item_id = scrapy.Field()
    one_item_name = scrapy.Field()
    one_item_nick = scrapy.Field()
    one_item_price_M = scrapy.Field()
    one_item_price_P = scrapy.Field()
    one_item_price_Prime = scrapy.Field()
    one_item_discount = scrapy.Field()


class PchomecQtyItem(scrapy.Item):
    qty_id = scrapy.Field()
    id_qty = scrapy.Field()
    price_m = scrapy.Field()
    price_p = scrapy.Field()
    price_prime = scrapy.Field()



# https://ecapi.pchome.com.tw/cdn/ecshop/cateapi/v1.5/region&region=DSAA&_callback=cb_ecshopCategoryRegion&5332770

# 第二层
# https://ecapi.pchome.com.tw/cdn/ecshop/cateapi/v1.5/region&sign=h24%252F3c&_callback=cb_ecshopCategoryRegion&5332770

# 侧边栏下班部门
# https://ecapi.pchome.com.tw/cdn/ecshop/cateapi/v1.6/region/DAAL/menu&_callback=jsonp_menu&5332492?_callback=jsonp_menu

# 侧边栏上半部分
# https://ecapi.pchome.com.tw/cdn/marketing/activity/v1/activity&regionid=DAAL&fields=ActId,ActName,Url&_callback=jsonp_activity&2666246

# 中间商品标题部分
# https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/activity/151485/prod&offset=1&limit=36&fields=Id,Nick,Pic,Price,Discount,isSpec,Name,isCarrier,isSnapUp,isBigCart,isPreOrder24h,PreOrdDate,isWarranty,isFresh,isBidding,isETicket,ShipType,isO2O&_callback=jsonp_prodlist?_callback=jsonp_prodlist

# 商品附件信息
# https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/prod/extra?id=DAAL0L-A900AOP8P,DAAL0L-A900AOP84,DAAL0L-A900AO2HX,DAAL0L-A900AO00U,DAAL0L-A900AMNEG,DAAL0L-A900AMNCK,DAAL0L-A900AMNBN,DAAL0L-A900AMNB9,DAAL0L-A900AMN9I,DAAL0L-A900AK2OK,DAAL0L-A900AK2OJ,DAAL0L-A900AB1ST,DAAL0L-A900AB1SM,DAAL0L-A900AB1RD,DAAL0L-A900A7PUR,DAAL0L-A9009CI8K,DAAL0L-A9009CI7C,DAAL0L-A90089I2O,DAAL0L-A90089I13&_callback=store_prodlist_extra&_callback=store_prodlist_extra

# 商品描述信息
# https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/prod/desc&id=DAAL0L-A900AOP8P,DAAL0L-A900AOP84,DAAL0L-A900AO2HX,DAAL0L-A900AO00U,DAAL0L-A900AMNEG,DAAL0L-A900AMNCK,DAAL0L-A900AMNBN,DAAL0L-A900AMNB9,DAAL0L-A900AMN9I,DAAL0L-A900AK2OK,DAAL0L-A900AK2OJ,DAAL0L-A900AB1ST,DAAL0L-A900AB1SM,DAAL0L-A900AB1RD,DAAL0L-A900A7PUR,DAAL0L-A9009CI8K,DAAL0L-A9009CI7C,DAAL0L-A90089I2O,DAAL0L-A90089I13&fields=Id,Slogan&_callback=jsonp_prodlist_slogan&2666246?_callback=jsonp_prodlist_slogan

# 商品剩余量
# https://ecapi.pchome.com.tw/ecshop/prodapi/v2/prod/button&id=DAAL0L-A900AOP8P,DAAL0L-A900AOP84,DAAL0L-A900AO2HX,DAAL0L-A900AO00U,DAAL0L-A900AMNEG,DAAL0L-A900AMNCK,DAAL0L-A900AMNBN,DAAL0L-A900AMNB9,DAAL0L-A900AMN9I,DAAL0L-A900AK2OK,DAAL0L-A900AK2OJ,DAAL0L-A900AB1ST,DAAL0L-A900AB1SM,DAAL0L-A900AB1RD,DAAL0L-A900A7PUR,DAAL0L-A9009CI8K,DAAL0L-A9009CI7C,DAAL0L-A90089I2O,DAAL0L-A90089I13&fields=Id,Qty,ButtonType,Price,isPrimeOnly&_callback=jsonp_prodlist_button?_callback=jsonp_prodlist_button

