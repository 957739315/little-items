import html_downloader,html_parser,url_manager,deal_json,corpus_output
import time
'''
爬取百度百科 Android 关键词相关词及简介并输出为一个HTML tab网页
Extra module:
BeautifulSoup
'''
class SpiderMain(object):
    def __init__(self,root_url):
        self.root_url=root_url
        self.urls=url_manager.UrlManager()
        self.downloader=html_downloader.HtmlDownloader()
        self.parser=html_parser.HtmlParser(root_url)
        self.deal_json=deal_json.DealJson()
        self.out_put=corpus_output.CorpusOutput()
        self.sum=0 #记录遍历过的数目


    def craw(self,page_start,page_end,lang_list,excel_name):
        page_urls =[]
        for i in range(page_start,page_end+1):
            page_urls.append(self.root_url+"/talks?page="+str(i))
        self.urls.add_page_urls(page_urls)
        # print(page_urls)
        excel_num=1  #表格号
        while self.urls.has_page_url():
            # print(self.urls.has_page_url())
            try:
                page_url=self.urls.get_page_url()
                print(page_url)
                headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3355.4 Safari/537.36"}
                page_content=self.downloader.download(page_url,retry_count=2,headers=headers)
                print(page_content)
                self.urls.add_video_urls(self.parser.parse(page_content))
                while self.urls.has_video_url():
                    print("\n\nanother video!!!")
                    self.sum += 1
                    lang_contents=self.deal_json.crawl_data(self.urls.get_video_url(),lang_list)
                    return_value=self.out_put.write_excel(excel_name+str(excel_num), lang_contents)
                    time.sleep(2)
                    if return_value==True:
                        excel_num += 1
                    else:
                        continue
            except Exception as e:
                print("craw failed!!"+str(e))
                break
        print(self.sum)



if __name__=="__main__":
    rooturl="https://www.ted.com"
    objSpider=SpiderMain(rooturl)
    #韩语ko,越南语vi,印尼语id，马来西亚语ms

    # objSpider.craw(1, 76, ["zh-cn", "id"],"中文-印尼")
    objSpider.craw(1, 76, ["zh-cn", "ms"], "中文-马来西亚")