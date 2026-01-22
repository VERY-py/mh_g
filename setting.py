import math
import random
import pygame
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
PLAYER_SIZE = (51, 51)
BULLET_RADIUS = 4
FPS = 60

language = 'RU'
worlds_en = [
    "START",
    "SETTINGS",
    "EXIT",
    "LANGUAGE",
    "FPS",
    "BACK"
]
worlds_ru = [
    "СТАРТ",
    "НАСТРОЙКИ",
    "ВЫХОД",
    "ЯЗЫК",
    "FPS",
    "НАЗАД"
]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 180, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MAP_png = "assets/map.png"
KT_T_png = "assets/PL_V1.png"
KT_Tr_png = "assets/PL_V1_d.png"
T_T_png = "assets/PL_V2.png"
T_Tr_png = "assets/PL_V2_d.png"
kursor_png = "assets/kursor.png"
knife_png = "assets/knife.png"
main_img_png = "assets/main_img.png"

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("goyda")
clock = pygame.time.Clock()
t_font = pygame.font.Font(None, 48)

def scale_surf(surf, scale, method='scale', keep_ratio=False):
    if surf is None:
        raise ValueError("Поверхность не может быть None")

    if isinstance(scale, tuple):
        new_size = scale
    else:
        if scale <= 0:
            raise ValueError("Коэффициент масштаба должен быть > 0")

        orig_w, orig_h = surf.get_size()
        if keep_ratio:
            scale_w = scale * orig_w
            scale_h = scale * orig_h
            min_scale = min(scale_w / orig_w, scale_h / orig_h)
            new_size = (int(orig_w * min_scale), int(orig_h * min_scale))
        else:
            new_size = (int(orig_w * scale), int(orig_h * scale))

    new_w, new_h = new_size
    if new_w <= 0 or new_h <= 0:
        new_size = (1, 1)

    if method == 'smooth':
        scaled = pygame.transform.smoothscale(surf, new_size)
    else:
        scaled = pygame.transform.scale(surf, new_size)

    scaled = scaled.convert_alpha() if surf.get_flags() & pygame.SRCALPHA else scaled.convert()

    return scaled

def check_circle_collision(circle_center, circle_radius, point):
    distance = math.hypot(point[0] - circle_center[0], point[1] - circle_center[1])
    if distance <= circle_radius:
        return True
    else:
        return False

def update_button(button_surface, sc, pos, mouse_pos):
    button_rect = button_surface.get_rect(topleft=pos)

    if button_rect.collidepoint(mouse_pos):
        darkened_surface = button_surface.copy()
        dark_overlay = pygame.Surface(button_surface.get_size(), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, 50))
        darkened_surface.blit(dark_overlay, (0, 0))

        sc.blit(darkened_surface, pos)
    else:
        sc.blit(button_surface, pos)

    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0] and button_rect.collidepoint(mouse_pos):
        return True

    return False

def create_button(text, font, button_width, button_height, text_color, bg_color=(57, 57, 57)):
    b_surface = pygame.Surface((button_width, button_height))
    b_surface.fill(bg_color)

    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(button_width // 2, button_height // 2))

    b_surface.blit(text_surface, text_rect)

    return b_surface

def draw_dict(sc, data, pos, fnt, fnth=1):
    x, y = pos
    line_height = fnt.get_height() + 5

    for key, value in data.items():
        text = f"{key}: {value}"
        text_surface = fnt.render(text, True, (244, 255, 0))
        text_rect = text_surface.get_rect()

        if fnth == 1:
            text_rect.left = x
        elif fnth == 2:
            text_rect.centerx = sc.get_width() // 2
        else:
            text_rect.right = sc.get_width()

        text_rect.top = y
        sc.blit(text_surface, text_rect)
        y += line_height

def brs_wpn(pl_inv, act_slot, player):
    if pl_inv[act_slot] is not None:

        r = random.randint(0, 180)

        if act_slot == 0:
            return 0
        else:
            rt_wpn = pygame.transform.rotate(pl_inv[act_slot][0], r)
            wp = scale_surf(rt_wpn, 0.5)
            b_wpn = pl_inv[act_slot]
            pl_inv[act_slot] = None

            b_wpn_pos = [player.x - 50, player.y - 50]
            b_wpns = (b_wpn, b_wpn_pos, wp)
            if act_slot != 0: act_slot -= 1
            return b_wpns
    return 0

MAP = scale_surf(pygame.image.load(MAP_png), 1.5)
KT_T = scale_surf(pygame.image.load(KT_T_png), 1.35)
KT_Tr = scale_surf(pygame.image.load(KT_Tr_png), 1.35)
T_T = scale_surf(pygame.image.load(T_T_png), 1.35)
T_Tr = scale_surf(pygame.image.load(T_Tr_png), 1.35)
kursor = pygame.image.load(kursor_png)
knife = pygame.image.load(knife_png)
main_img = pygame.image.load(main_img_png)

hrc_glock = [200, 20, 3, 9, 20, False]  # shot_time, bullet_speed, rasb, player_speed, mgz, aftmt
hrc_svd = [700, 34, 0, 7, 5, False]
hrc_ak = [150, 20, 5, 8, 30, True]
hrc_m4a1_s = [120, 25, 2, 8, 20, True]

wpn_glock_is = [pygame.image.load("assets/glock41.png"), hrc_glock, "glock"]
wpn_svd_is = [scale_surf(pygame.image.load("assets/svd.png"), 0.4), hrc_svd, "svd"]
wpn_ak_is = [scale_surf(pygame.image.load("assets/ak-47.png"), 0.2), hrc_ak, "ak-47"]
wpn_m4a1_s_is = [pygame.image.load("assets/m4a1-s.png"), hrc_m4a1_s, "m4a1-s"]

wpn_glock = wpn_glock_is.copy()
wpn_svd = wpn_svd_is.copy()
wpn_ak = wpn_ak_is.copy()
wpn_m4a1_s = wpn_m4a1_s_is.copy()

os_wpn = [wpn_svd, wpn_ak, wpn_m4a1_s]
vt_wpn = [wpn_glock]