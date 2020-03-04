import scrapy


class XieChengItem(scrapy.Item):
    title = scrapy.Field()
    addr = scrapy.Field()
    value = scrapy.Field()
    recommend = scrapy.Field()
    comment_num = scrapy.Field()
    low_price = scrapy.Field()

    closerate = scrapy.Field()
    meetingroom = scrapy.Field()
    type = scrapy.Field()
    sum = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    geohash = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    adcode = scrapy.Field()

    brand = scrapy.Field()
