from setting import *
import sys
from Classes.player import Player
from Classes.camera import Camera
from Classes.bullet import Bullet

pygame.init()

def main_menu(scr):
    global m
    if language == 'RU':
        b_start = create_button(worlds_ru[0], t_font, 300, 100, (203, 235, 73))
        b_setting = create_button(worlds_ru[1], t_font, 300, 100, (203, 235, 73))
        b_exit = create_button(worlds_ru[2], t_font, 300, 100, (203, 235, 73))
    elif language == 'EN':
        b_start = create_button(worlds_en[0], t_font, 300, 100, (203, 235, 73))
        b_setting = create_button(worlds_en[1], t_font, 300, 100, (203, 235, 73))
        b_exit = create_button(worlds_en[2], t_font, 300, 100, (203, 235, 73))
    else:
        b_start = False
        b_setting = False
        b_exit = False

    pygame.mouse.set_visible(1)
    run = True
    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                m = 0
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    run = False
                    m = 0

        scr.fill((100, 100, 100))
        scr.blit(main_img, (0, 0))
        b_start_pr = update_button(b_start, scr, (750, 300), pygame.mouse.get_pos())
        if b_start_pr: run, m = False, 2
        b_setting_pr = update_button(b_setting, scr, (750, 450), pygame.mouse.get_pos())
        if b_setting_pr: run, m = False, 3
        b_exit_pr = update_button(b_exit, scr, (750, 750), pygame.mouse.get_pos())
        if b_exit_pr: run, m = False, 0
        pygame.display.flip()
        clock.tick(FPS)

def settings(scrn):
    global m
    if language == 'RU':
        b_lang = create_button(worlds_ru[3], t_font, 300, 100, (203, 235, 73))
        b_fps = create_button(worlds_ru[4], t_font, 300, 100, (203, 235, 73))
        b_exit = create_button(worlds_ru[5], t_font, 300, 100, (203, 235, 73))
    elif language == 'EN':
        b_lang = create_button(worlds_en[3], t_font, 300, 100, (203, 235, 73))
        b_fps = create_button(worlds_en[4], t_font, 300, 100, (203, 235, 73))
        b_exit = create_button(worlds_en[5], t_font, 300, 100, (203, 235, 73))
    else:
        b_lang = False
        b_fps = False
        b_exit = False
    pygame.mouse.set_visible(1)
    run = True
    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                m = 0
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    run = False
                    m = 1

        scrn.fill((100, 100, 100))
        scrn.blit(main_img, (0, 0))
        b_lang_pr = update_button(b_lang, scrn, (750, 300), pygame.mouse.get_pos())
        # if b_lang_pr: run, m = False, 2
        b_fps_pr = update_button(b_fps, scrn, (750, 450), pygame.mouse.get_pos())
        # if b_fps_pr: run, m = False, 3
        b_exit_pr = update_button(b_exit, scrn, (750, 600), pygame.mouse.get_pos())
        if b_exit_pr: run, m = False, 1
        pygame.display.flip()
        clock.tick(FPS)

def game(scre):
    global m
    player = Player(620, 350, KT_T)
    camera = Camera(player)

    pygame.mouse.set_visible(0)
    map_mask = pygame.mask.from_surface(MAP)

    bullets = []
    pl_inv = ["knife", wpn_glock, wpn_ak]
    b_wpns = []
    last_shot_time = 0
    shot_time = 0
    bullet_speed = 0
    mgz = 0
    p = False
    rasb = 0
    pl_speed = 0
    aftmt = False
    act_slot = 0
    is_knife = True

    f1 = False
    line_dr = False
    running = True
    b_wpns.append(spawn_wpn(wpn_m4a1_s, (300, 300)))
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                m = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    m = 1
                if event.key == pygame.K_r:
                    p = True
                if event.key == pygame.K_g:
                    b = brs_wpn(pl_inv, act_slot, player)
                    if b != 0: b_wpns.append(b)
                if event.key == pygame.K_e:
                    for wpno in b_wpns:
                        wpn, wpn_pos, wp = wpno
                        if check_circle_collision((player.x, player.y), 100, wpn_pos):
                            b_wpns.remove(wpno)
                            if wpn in os_wpn:
                                if pl_inv[2] is not None:
                                    b = brs_wpn(pl_inv, 2, player)
                                    if b != 0: b_wpns.append(b)
                                pl_inv[2] = wpn
                                act_slot = 2
                            elif wpn in vt_wpn:
                                if pl_inv[1] is not None:
                                    b = brs_wpn(pl_inv, 1, player)
                                    if b != 0: b_wpns.append(b)
                                pl_inv[1] = wpn
                                act_slot = 1
                if event.key == pygame.K_F1:
                    if f1:
                        f1 = False
                    else:
                        f1 = True
                if event.key == pygame.K_1:
                    act_slot = 0
                elif event.key == pygame.K_2:
                    if pl_inv[1] is not None:
                        act_slot = 1
                elif event.key == pygame.K_3:
                    if pl_inv[2] is not None:
                        act_slot = 2
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if act_slot == 0:
                        if pl_inv[1] is not None:
                            act_slot = 1
                        elif pl_inv[2] is not None:
                            act_slot = 2
                    elif act_slot == 1:
                        if pl_inv[2] is not None:
                            act_slot = 2
                        else:
                            act_slot = 0
                    elif act_slot == 2:
                        act_slot = 0
                elif event.button == 5:
                    if act_slot == 0:
                        if pl_inv[2] is not None:
                            act_slot = 2
                        elif pl_inv[1] is not None:
                            act_slot = 1
                    elif act_slot == 1:
                        act_slot = 0
                    elif act_slot == 2:
                        if pl_inv[1] is not None:
                            act_slot = 1
                        else:
                            act_slot = 0
                if not aftmt:
                    if event.button == 1 or event.button == 1 and event.button == 2:
                        current_time = pygame.time.get_ticks()
                        if current_time - last_shot_time > shot_time:
                            last_shot_time = current_time
                            bal_end = player.get_st_end()
                            bullets.append(Bullet(bal_end[0], bal_end[1], player.angle, bullet_speed, rasb, is_knife))

        if act_slot == 0:
            shot_time = 400
            pl_speed = 11
            rasb = 0
            bullet_speed = 10
            mgz = 0
            aftmt = True
            is_knife = True
        elif act_slot == 1:
            if pl_inv[1] is not None:
                shot_time = pl_inv[1][1][0]
                bullet_speed = pl_inv[1][1][1]
                rasb = pl_inv[1][1][2]
                pl_speed = pl_inv[1][1][3]
                mgz = pl_inv[1][1][4]
                aftmt = pl_inv[1][1][5]
                is_knife = False
        elif act_slot == 2:
            if pl_inv[2] is not None:
                shot_time = pl_inv[2][1][0]
                bullet_speed = pl_inv[2][1][1]
                rasb = pl_inv[2][1][2]
                pl_speed = pl_inv[2][1][3]
                mgz = pl_inv[2][1][4]
                aftmt = pl_inv[2][1][5]
                is_knife = False

        rasb = player.update(keys, pl_speed, map_mask, rasb)

        camera.update()

        mx, my = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        if aftmt:
            if mouse[0]:
                if mgz != 0:
                    mgz -= 1
                    current_time = pygame.time.get_ticks()
                    if current_time - last_shot_time > shot_time:
                        last_shot_time = current_time
                        bal_end = player.get_st_end()
                        bullets.append(Bullet(bal_end[0], bal_end[1], player.angle, bullet_speed, rasb, is_knife))
                elif mgz == 0:
                    if p:
                        p = False
                        pl_inv[act_slot][1] = 1  # доделать перезарядку warn
        if mouse[2]:
            line_dr = True

        for bullet in bullets[:]:
            if bullet.update(map_mask):
                bullets.remove(bullet)

        if act_slot == 0:
            txt_wpn = "knife"
        else:
            if pl_inv[act_slot] is None:
                txt_wpn = "None"
            else:
                txt_wpn = pl_inv[act_slot][2]
        F1 = {
            "Разброс" : rasb*2,
            "X, Y" : (player.x, player.y),
            "Угол поворота" : player.angle,
            "Скорость" : pl_speed,
            "Оружие" : txt_wpn,
            "Активный слот" : act_slot,
            "Оружие автомат." : aftmt,
            "Is knife": is_knife
        }

        scre.fill((100, 100, 100))

        scre.blit(MAP, (camera.offset_x, camera.offset_y))

        for wpn, wpn_pos, wp in b_wpns:
            scre.blit(wp, (camera.offset_x + wpn_pos[0], camera.offset_y + wpn_pos[1]))

        for bullet in bullets:
            bullet.draw(scre, camera)

        if line_dr:
            pygame.draw.line(scre, (255, 0, 0),
                             ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
                             pygame.mouse.get_pos(), 2)
            line_dr = False

        player.draw(scre, camera)

        if act_slot == 0:
            scre.blit(knife, (10, 30))
        elif act_slot == 1:
            if pl_inv[1] is not None:
                scre.blit(pl_inv[1][0], (10, 30))
        elif act_slot == 2:
            if pl_inv[2] is not None:
                scre.blit(pl_inv[2][0], (10, 30))

        if f1:
            draw_dict(scre, F1, (0, 0), t_font, 3)

        scre.blit(kursor, ((mx - 21), (my - 21)))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    rnn = True
    m = 1
    while rnn:
        if m == 1:
            main_menu(screen)
        elif m == 2:
            game(screen)
        elif m == 3:
            settings(screen)
        elif m == 0:
            rnn = False
    pygame.quit()
    sys.exit()
