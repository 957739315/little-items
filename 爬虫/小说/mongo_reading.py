#coding:utf-8
import pymongo
import os
import urllib.request
from lxml import etree



client = pymongo.MongoClient('localhost',27017)
reading = client['reading']
sheet_words = reading['sheet_words']

url = 'http://www.17k.com/list/493239.html'
response = urllib.request.urlopen(url)
html = response.read().decode("utf-8")
tree = etree.HTML(html)
dom = tree.xpath('//a[@target="_blank"][@title]/@href')

for i in dom:
    data = {
        'words':"http://www.17k.com" + i
    }
    sheet_words.insert_one(data)


# $lt/$lte/$gt/$gte/$ne，依次等价于</<=/>/>=/!=。（l表示less g表示greater e表示equal n表示not  ）
try:
    os.mkdir("修罗武神小说")
except FileExistsError:
    pass
os.chdir("修罗武神小说")
for item in sheet_words.find():
    filename = "修罗武神"
    with open( filename,"a+") as f:
        contents = urllib.request.urlopen(item["words"])
        responses = contents.read().decode("utf-8")
        trees = etree.HTML(responses)
        title = trees.xpath('//div[@class="readAreaBox content"]/h1/text()')
        word = trees.xpath("/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/text()")
        a = ''.join(title)
        b = ''.join(word)
        f.write(a)
        f.write(b)
        #print(''.join(title))






#mongod -dbpath "E:\mongodb\data\db"
