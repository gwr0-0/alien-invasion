import pygame
from pygame.sprite import Sprite


class AlienBullet(Sprite):
    """管理外星人发射的子弹"""

    def __init__(self, ai_settings, screen, alien):
        super().__init__()
        self.screen = screen

        # 在 (0,0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.top

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """向下移动子弹"""
        # 更新表示子弹位置的小数值
        self.y += self.speed_factor
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
