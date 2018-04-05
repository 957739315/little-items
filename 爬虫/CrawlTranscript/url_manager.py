class UrlManager(object):
    def __init__(self):
        self.page_urls=set()
        self.video_urls=set()

    def add_page_urls(self,urls):
        if urls is None or len(urls)==0:
            return
        for url in urls:
            self.page_urls.add(url)

    def add_video_urls(self,urls):
        if urls is None or len(urls)==0:
            return
        for url in urls:
            self.video_urls.add(url+"/transcript.json?language=")
    def has_page_url(self):
        return len(self.page_urls)>0

    def has_video_url(self):
        return len(self.video_urls)>0

    def get_page_url(self):
        temp_url=self.page_urls.pop()
        return temp_url

    def get_video_url(self):
        temp_url=self.video_urls.pop()
        return temp_url

























