import time
from urllib import request
import json

class DealJson(object):

    def crawl_data(self,video_url,lang_list):
        '''
        爬取lang_list所需的语种，保存到字典{“语种名”：[语料]}
        '''
        lang_num=0
        if video_url is None or lang_list is None:
            return
        lang_contents=dict()
        for lang in lang_list:
            lang_contents[lang] = self.crawl_one_lang(video_url,lang)
            if  lang_contents[lang] == "quit":
                break
            if lang_contents[lang] != None :
                lang_num+=1

        #如果查找的语种都没有返回False,
        if lang_num<len(lang_list):
            print("语种少于"+str(len(lang_list))+"种！！"+video_url)
            print("-----quit")
            return None
        else:
            return lang_contents



    def crawl_one_lang(self,video_url,lang,retry_count=2):
        time.sleep(2)
        cur_url = video_url + lang
        contents = list()
        try:
            with request.urlopen(cur_url, timeout=10) as response:
                content = json.loads(response.read())
                if content is not None:
                    for cues in content["paragraphs"]:
                        for cue in cues["cues"]:
                            contents.append(cue["text"])
            print("suceessful!!!  " + lang)
            return  contents
        except Exception as e:
            print('deal_json   crawl_data exception.' + str(e) + " No " + lang)
            if retry_count > 0:
                if str(e) == "<urlopen error timed out>":
                    time.sleep(20)
                    return self.crawl_one_lang(video_url, lang, retry_count - 1)
                elif str(e) == "HTTP Error 429: Rate Limited too many requests.":
                    time.sleep(60)
                    return self.crawl_one_lang(video_url,lang,retry_count-1)
                elif str(e) == "HTTP Error 404: Not Found":
                    return "quit"
                else:
                    print(cur_url)
                    time.sleep(10)
                    return self.crawl_one_lang(video_url,lang,retry_count-1)
