import sys
import pygame
from pygame.sprite import Group #类似列表

from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

'''快捷键：P键或点击Play——开始游戏；Q键——退出游戏；空格键——射击；左右键——移动飞船'''

'''
待改进：
1、游戏节奏太快，想重置游戏节奏；
2、增加Help说明按钮，显示说明信息；
3、实现外星人也能射击；
4、给飞船添加盾牌；
5、可以改变飞船的子弹方向
6、pygame.mixer添加爆炸声和射击声
7、实现网页端，提供给别人玩

'''

def run_game():

    #初始化哟偶系并创建一个屏幕对象
    pygame.init()

    #设置title
    pygame.display.set_caption("Alien Invasion")

    ai_settings=Settings()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))

    #创建一艘飞船
    ship=Ship(ai_settings,screen)

    #创建一个用于存储子弹的编组
    bullets=Group()

    #创建Alien实例
    aliens=Group()
    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #创建一个用于存储游戏统计信息的实例,并创建记分牌
    stats=GameStats(ai_settings)
    sb=Scoreboard(ai_settings,screen,stats)

    #创建Play按钮
    play_button=Button(ai_settings,screen,"Play")


    #开始游戏的主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            #检测到有事件操作飞船，更新飞船状态
            ship.update()

            gf.update_bullets(ai_settings,screen,stats,sb, ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,screen,sb,ship,aliens,bullets)

        #每次循环都重绘屏幕
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)


run_game()
