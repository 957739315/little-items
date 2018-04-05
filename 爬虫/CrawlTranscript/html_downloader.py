from http import cookiejar
from urllib import request,error
from urllib.parse import urlparse
import time

'''
如下是使用 Python3 内置模块实现的一个比上一篇稍微健壮一点点的下载器。
通过内置 urllib 进行 header 设置或者代理设置或者启用会话，支持简单的 HTTP CODE 5XX 重试机制，支持 GET\POST。
（实际项目考虑和封装的要比这更加健壮）
'''
class HtmlDownloader(object):
    def download(self,url,retry_count=3,headers=None,proxy=None,data=None):
        '''
              :param url: 准备下载的 URL 链接
              :param retry_count: 如果 url 下载失败重试次数
              :param headers: http header={'X':'x', 'X':'x'}
              :param proxies: 代理设置 proxies={"https": "http://12.112.122.12:3212"}
              :param data: 需要 urlencode(post_data) 的 POST 数据
              :return: 网页内容或者 None
        '''
        if url is None:
            return None
        try:
            req=request.Request(url,headers=headers,data=data)

            # 初始化一个CookieJar来处理Cookie
            #Cookie 的操蛋之处，分析时建议开启隐身模式等，不然就面对清空 Cookie 大法了，清空 Cookie 对于爬虫网站分析至关重要，一定要 get 到。
            cookie=cookiejar.CookieJar()
            #创建HTTP处理器
            cookie_process=request.HTTPCookieProcessor(cookie)
            opener=request.build_opener()
            if proxy:
                '''使用urlparse()后被分成6个部分：scheme = 'http', netloc = 'www.baidu.com', path = 'index.html'
                paramters = 'user'.query = 'id=5', fragment = 'comment' 
                urlparse还有带参数的是使用方法

                res=urlparse(urlstring,scheme=' ',allow_fragment=True)
                scheme是默认的协议，如果urlstring没有带协议，则使用scheme中的协议，若是有，则仍然使用urlstring中协议
                allow_fragment即是否忽略fragment,如果是False，fragment就被解析为path、paramenters或者query中的一部分   
                '''
                proxies={urlparse(url).scheme:proxy}

                #设置全局代理服务器
                '''一些网站会有相应的反爬虫措施，例如很多网站会检测某一段时间某个IP的访问次数，如果
                访问频率太快以至于看起来不像正常访客，它可能就会会禁止这个IP的访问。所以我们需要设置
                一些代理服务器，每隔一段时间换一个代理，就算IP被禁止，依然可以换个IP继续爬取。'''
                opener.add_handler(request.ProxyHandler(proxies))
            conopen=opener.open(req)
            time.sleep(1)
            content=conopen.read()

        except error.URLError as e:
            print("HtmlDownLoader download error:",e.reason)
            content=None
            if retry_count>0:
                if hasattr(e,'code') and 500<=e.code<600:
                # 说明是 HTTPError 错误且 HTTP CODE 为 5XX 范围说明是服务器错误，可以尝试再次下载
                    return self.download(url,retry_count-1,headers,proxy,data)
        return content
























