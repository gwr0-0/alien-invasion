class Settings:
    """存储所有设置"""

    def __init__(self):
        """"初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.hg_color = (230, 230, 230)

        # 飞船设置
        self.ship_speed_factor = 1.5

        # 子弹设置
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        # 同屏最大子弹量
        self.bullets_allowed = 3

        # 外星人设置
        # 横向移动速度
        self.alien_speed_factor = 1
        # 纵向移动速度
        self.fleet_drop_speed = 10
        # 1右移，-1左移
        self.fleet_direction = 1
