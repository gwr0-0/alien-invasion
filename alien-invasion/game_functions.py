import sys
import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果没有达到限制，就发射一颗子弹"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """按键松开"""
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = False


def check_events(ai_settings, screen, ship, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings, screen, ship, aliens, bullets):
    """更新屏幕上对图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.hg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 让最近绘制对屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹位置
    bullets.update()

    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, aliens, bullets):
    # 检查是否击中，同时删除子弹和机器人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # 检查进度，重置子弹和外星人
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, aliens)


def get_number_aliens_x(screen_width, alien_width):
    """计算外星人数量，通过屏幕宽度和机器人宽度"""
    # 可用于放置外星人的水平空间为屏幕宽度减去外星人宽度的2倍
    available_space_x = screen_width - 2 * alien_width
    # 一行可容纳外星人数量，确保是一个整数
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x


def create_alien(ai_settings, screen, aliens, alien_width, alien_number):
    # 创建一个外星人
    alien = Alien(ai_settings, screen)
    # 计算位置，要向右推一个宽度，然后将宽度*2*当前数量
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    # 加入当前行
    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可以容纳多少个外星人
    # 外星人间隔为外星人宽度
    alien = Alien(ai_settings, screen)
    # 机器人宽度
    alien_width = alien.rect.width
    # 机器人数量
    number_alien_x = get_number_aliens_x(ai_settings.screen_width, alien_width)

    # 创建一行外星人
    for alien_number in range(number_alien_x):
        create_alien(ai_settings, screen, aliens, alien_width, alien_number)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边边缘时的策略"""
    for alien in aliens.sprites():
        if alien.check_edge():
            ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, aliens):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
