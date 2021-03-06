import random
import sys
import pygame

from alien_bullet import AlienBullet
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


def fire_aliens_bullet(ai_settings, screen, aliens, aliens_bullets):
    """如果没有达到限制，就发射一颗子弹"""
    if len(aliens_bullets) < ai_settings.bullets_allowed:
        new_bullet = AlienBullet(ai_settings, screen, random.choice(aliens.sprites()))
        aliens_bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """按键松开"""
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = False


def check_events(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets, mouse_x, mouse_y):
    """点击Play按钮时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 重置游戏屏幕显示
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, aliens_bullets, play_button):
    """更新屏幕上对图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for aliens_bullet in aliens_bullets.sprites():
        aliens_bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    sb.show_score()

    # 如果游戏处于非活跃状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制对屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹位置
    bullets.update()

    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, aliens, bullets):
    # 检查是否击中，同时删除子弹和机器人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()

    # 检查进度，重置子弹和外星人
    if len(aliens) == 0:
        bullets.empty()

        # 提高等级
        stats.level += 1
        sb.prep_level()
        ai_settings.increase_speed()

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
            check_fleet_direction(ai_settings, aliens)


def check_fleet_direction(ai_settings, aliens):
    """将整群机器人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """检查是否有外星人抵达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, aliens_bullets):
    check_fleet_edges(ai_settings, aliens)
    update_aliens_bullet(ai_settings, screen, aliens, aliens_bullets)
    aliens.update()

    # 检测外星人和飞船直接的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    # 检查是否有外星人抵达屏幕底端
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def update_aliens_bullet(ai_settings, screen, aliens, aliens_bullets):
    fire_aliens_bullet(ai_settings, screen, aliens, aliens_bullets)

    aliens_bullets.update()
    for aliens_bullet in aliens_bullets.copy():
        if aliens_bullet.rect.bottom >= ai_settings.screen_height:
            print("remove")
            aliens_bullets.remove(aliens_bullet)


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    print("Ship hit!")
    if stats.ships_left > 0:
        # 生命值减一
        stats.ships_left -= 1
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()
    else:
        stats.game_active = False
