# coding=utf-8
import json
import os
import re
import csv
import time
from urllib import request
import codecs



'''
Python3.X 动态页面爬取（逆向解析）实例

'''

class CrawlTED(object):
    def __init__(self):
        self.headers = {
            'User-Agent': '	Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            # 'X-Requested-With': 'XMLHttpRequest',
            'Host': 'www.ted.com',
            # 'Referer': 'https://www.ted.com/talks/amis…your_wandering_mind/transcript'.format(urllib.parse.quote(self.search_word)),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        self.success_video=0
        self.success_item=0


    def _crawl_data(self,video_id,lang_list,proxy=None,retry_count=2):
        '''
        爬取lang_list所需的语种，要求全部都有才进行爬取，没有则丢弃
        '''
        #urls=[]  #vi越南语，id印尼语，ms马来西亚语，zh_cn中文，en英文
        contents=dict()
        for lang in lang_list:
            time.sleep(2)
            url= "https://www.ted.com/talks/"+str(video_id)+"/transcript.json?language="+lang
            #urls.append(url)
            try:
                with request.urlopen(url, timeout=10) as response:
                    content = response.read()
                    contents[lang]=content
            except Exception as e:
                contents.clear()  #将内容置空
                print('_crawl_data exception.'+str(e)+'!!   No '+lang+'!!\n\n')
                if retry_count > 0:
                    if str(e)=="<urlopen error timed out>":
                        time.sleep(20)
                        # 说明是 HTTPError 错误且 HTTP CODE 为 5XX 范围说明是服务器错误，可以尝试再次下载
                        return self._crawl_data(video_id,lang_list, retry_count - 1)
                    if str(e)=="HTTP Error 429: Rate Limited too many requests.":
                        time.sleep(30)
                    if str(e)=="HTTP Error 404: Not Found":
                        contents=None
                        break

                    #<urlopen error [Errno 11001] getaddrinfo failed>  没网络

        return contents

    def _parse_data(self, lang_list,contents):
        '''
        对获取到的json数据进行解析
        '''

        if contents is None:
            return None
        lang_results=dict()
        for lang in lang_list:
            lang_results[lang]=""
            try:
                data_list = json.loads(contents[lang])
                #print(data_list)
                for data in data_list["paragraphs"]:
                    temp="" #一个cue保存一段文本，作为列表中一个元素
                    for cue in data["cues"]:
                        lang_results[lang]+=cue["text"]
                    #lang_results[lang].append(temp)
            except Exception as e:
                print('_parse_data exception.'+str(e)+'\n\n')
        return self.deal_split(lang_results)

    def deal_split(self, lang_results):
        #print(lang_results)
        if lang_results is None or len(lang_results)<=0:
            print("deal_align is None")
            return None
        else:
            for k,v in lang_results.items():
                # 将换行符替换为空格
                v=v.replace('\n',' ')
                lang_results[k]=re.split(r'[?;.]',v)
                while '' in lang_results[k]:
                    lang_results[k].remove('')

            print(lang_results)
            return lang_results



    def _save_text(self,writer,lang_list, lang_results):
        '''
            将爬取到的内容写入CSV文件
        '''
        if lang_results is None:
            print('save variable is None!')
            return
        try:
            # 获取每种语料中的列表长度，即句子数，获取第一种语料的句子数

            # 判断句子数是否相同;判断内容是否为空
            get_length = len(lang_results[lang_list[0]])
            flag=True #判断是否能够一句一句对齐
            print("句子数：\n")
            print(lang_list[0]+str(get_length))
            for key in lang_list[1:]:
                print(key + str(len(lang_results[key])))
                if get_length == len(lang_results[key]):
                    continue
                else:
                    print("句子数没对齐！！！\n\n")
                    flag=False


            # 如果对齐了，就分开保存。将内容写入CSV文件
            if flag is True and get_length!=0:
                for i in range(get_length):
                    data = []
                    for key in lang_list:
                        data.append(lang_results[key][i])
                    writer.writerow(data)

                print("save  OK!!!\n\n\n")
                self.success_item+=get_length
                self.success_video += 1

            #如果没办法一句句对齐，则整个文本对齐
            if flag is False and get_length!=0:
                data = []
                for key in lang_list:
                    temp=""
                    for i in lang_results[key]:
                        temp+=i
                    data.append(temp)
                writer.writerow(data)

                print("save  OK!!!\n\n\n")
                self.success_item+=get_length
                self.success_video += 1


        except Exception as e:
            print("_save_text exception!!! "+str(e)+'\n\n')




    def go(self,id_start,id_end,lang_list,filename):
        with open(filename, "a", encoding='UTF-8', newline='') as file:
            # 写表头
            #file.write(codecs.BOM_UTF8)
            writer = csv.writer(file, dialect="excel")
            #writer.writerow(["越南语","印尼语","马来西亚语"])

            for video_id in range(id_start,id_end+1):
                print(video_id)
                time.sleep(1) #防止封IP
                lang_results=self._parse_data(lang_list,self._crawl_data(video_id,lang_list))
                if lang_results is None or len(lang_results)<=0:
                    continue
                try:
                    self._save_text(writer,lang_list,lang_results)
                except Exception as e:
                    print("go exception!"+str(e)+"\n\n\n")

            file.close()

        print("成功保存条数："+str(self.success_item))
        print("成功爬取视频数："+str(self.success_video))


if __name__ == '__main__':
    CrawlTED().go(1036,1200,['vi','id','ms'],"陈妙容_第一次作业.csv")
