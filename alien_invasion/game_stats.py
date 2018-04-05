class GameStats():
    '''跟踪游戏的统计信息'''
    def __init__(self,ai_settings):
        '''初始化统计信息'''
        self.ai_settings=ai_settings
        self.reset_stats()
        self.game_active=False

        #任何情况下都不应重置最高得分
        self.high_score=int(self.read_high_score_file())


    def reset_stats(self):
        '''初始化在游戏运行期间可能变化的统计信息'''
        self.ships_left=self.ai_settings.ship_limit
        self.score=0
        self.level=1

    def read_high_score_file(self):
        '''读取历史最高分'''
        filename = "high score.txt"
        try:
            with open(filename) as file:
                return file.read()
        except FileNotFoundError:
            return 0
