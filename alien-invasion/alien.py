import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """单个外星人"""

    def __init__(self, ai_settings, screen):
        """初始化外星人并设置初始位置"""
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        # 加载外星人图像，并设置其rect属性
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        """"在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edge(self):
        """检查是否到底边缘"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """向左或向右移动外星人"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x