
'''
知乎登录(使用手机号登录)
Extra module:
requests
BeautifulSoup
'''

from ZhiHu_login import ZhiHuLogIn

class ZhiHuMain(object):
    # def __int__(self):
    #     self.login=ZhiHuLogIn()

    def run(self):
        # self.login.login('15018371059','hong222hai')
        ZhiHuLogIn().login('15018371059', 'hong222hai')

if __name__=="__main__":
    ZhiHuMain().run()