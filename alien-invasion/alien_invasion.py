import pygame

import game_functions as gf
from settings import Settings
from game_stats import GameStats
from ship import Ship
from pygame.sprite import Group
from button import Button


def run_game():
    # 初始化pygame、设置和屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建按钮
    play_button = Button(screen, "Play")

    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats()

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, aliens)

    # 开始游戏主循环
    while True:
        # 监视事件，刷新屏幕
        gf.check_events(ai_settings, screen, stats, play_button, ship, bullets)
        # 游戏活动状态
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, aliens, bullets)
            gf.update_aliens(ai_settings, aliens)
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button)


run_game()
