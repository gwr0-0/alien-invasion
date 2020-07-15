class Settings:
    """存储所有设置"""

    def __init__(self):
        """"初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        # 同屏最大子弹量
        self.bullets_allowed = 3

        # 外星人设置
        # 纵向移动速度
        self.fleet_drop_speed = 10
        # 1右移，-1左移
        self.fleet_direction = 1

        # 记分
        self.alien_points = 1

        # 加速游戏
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """会随游戏进行而变化的设置"""
        # 外星人横向移动速度
        self.ship_speed_factor = 1.5
        # 子弹速度
        self.bullet_speed_factor = 1
        # 飞船设置
        self.alien_speed_factor = 1

    def increase_speed(self):
        """加速游戏设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
