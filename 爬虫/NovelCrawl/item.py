#-*-coding:utf-8-*-

# #问题1：python3引进scrapy引入不成功？
# import scrapy
#
#
#
# #问题2：这里的item怎么理解? 这个是属于类的应用
# class NovelCrawlItem(scrapy.item):
#     list_name=scrapy.Field()
#     name=scrapy.Field()
#     title=scrapy.Field()
#     link=scrapy.Field()
#     words=scrapy.Field()


import json

#
# numbers=[1,1,1,1,1,1,1]
# with open('test2.json','w') as file:
#     json.dump(numbers,file)

with open('test2.json') as file:
    numbers=json.load(file)
print(numbers)
