import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class HtmlParser(object):
    def __init__(self,root_url):
        self.root_url=root_url

    def parse(self,page_content,html_encode="utf-8"):
        if page_content is None:
            return
        #对网页内容采用html.parser解析器进行解析
        soup=BeautifulSoup(page_content,"html.parser",from_encoding=html_encode)

        video_urls=self.get_video_urls(soup)
        print(video_urls)
        return video_urls

    #url="https://www.ted.com"
    def get_video_urls(self,soup):
        video_urls=set()
        links = soup.find_all("a", class_="ga-link", href=re.compile(r"/talks/\w+"))
        for link in links:
            url_path=self.root_url+link["href"]
            video_urls.add(url_path)
        print(len(video_urls))
        return video_urls















































