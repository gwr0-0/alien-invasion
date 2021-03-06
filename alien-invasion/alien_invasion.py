import pygame

import game_functions as gf
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
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

    # 创建一个用于存储游戏统计信息的实例，和记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    aliens_bullets = Group()
    gf.create_fleet(ai_settings, screen, aliens)

    # 开始游戏主循环
    while True:
        # 监视事件，刷新屏幕
        gf.check_events(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets)
        # 游戏活动状态
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, aliens_bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, aliens_bullets, play_button)


run_game()
