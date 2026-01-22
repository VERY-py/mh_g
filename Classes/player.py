from setting import *

class Player:
    def __init__(self, x, y, image_path=None):
        self.x = x
        self.y = y
        self.angle = 0
        self.turn_speed = 3
        self.z = 0
        self.size = PLAYER_SIZE

        if image_path:
            self.original_image = image_path.convert_alpha()
        else:
            self.original_image = pygame.Surface(self.size, pygame.SRCALPHA)
            pygame.draw.rect(self.original_image, GREEN, (0, 0, self.size[0], self.size[1]))
            pygame.draw.rect(self.original_image, BLACK, (0, 0, self.size[0], self.size[1]), 2)

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.original_image)

    def update(self, keys, speed, map_mask, rasbr):
        old_x, old_y, old_angle, speed_n = self.x, self.y, self.angle, speed

        cursor_x, cursor_y = pygame.mouse.get_pos()

        dx = cursor_x - (SCREEN_WIDTH // 2)
        dy = cursor_y - (SCREEN_HEIGHT // 2)

        angle_rad = math.atan2(dy, dx)

        angle_deg = math.degrees(angle_rad)
        if angle_deg > 360:
            angle_deg -= 360

        self.angle = int(angle_deg) + 90

        rotated_image = pygame.transform.rotate(self.original_image, -self.angle)
        rotated_mask = pygame.mask.from_surface(rotated_image)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))

        offset = (rotated_rect.left, rotated_rect.top)

        if map_mask.overlap(rotated_mask, offset):
            self.angle = old_angle
        else:
            self.image = rotated_image
            self.mask = rotated_mask
            self.rect = rotated_rect

        if keys[pygame.K_LSHIFT]:
            speed_n -= 4
            rasbr -= 1
        elif keys[pygame.K_LCTRL]:
            speed_n -= 6
            rasbr -= 2
        else:
            speed_n = speed

        dx, dy = 0, 0
        g = 0
        if keys[pygame.K_w]:
            dy -= speed_n // 2
            g = 1
        if keys[pygame.K_s]:
            dy += speed_n // 2
            g = 1
        if keys[pygame.K_a]:
            dx -= speed_n // 2
            g = 1
        if keys[pygame.K_d]:
            dx += speed_n // 2
            g = 1
        if g == 1:
            rasbr += 5

        new_x = self.x + dx
        new_y = self.y + dy
        new_rect = self.image.get_rect(center=(new_x, new_y))

        offset = (new_rect.left, new_rect.top)

        if not map_mask.overlap(self.mask, offset):
            self.x = new_x
            self.y = new_y
            self.rect = new_rect
        else:
            if dx != 0 or dy != 0:
                temp_x = self.x + dx
                temp_rect = self.image.get_rect(center=(temp_x, self.y))
                temp_offset = (temp_rect.left, temp_rect.top)

                if not map_mask.overlap(self.mask, temp_offset):
                    self.x = temp_x
                    self.rect = temp_rect
                    return rasbr

                temp_y = self.y + dy
                temp_rect = self.image.get_rect(center=(self.x, temp_y))
                temp_offset = (temp_rect.left, temp_rect.top)

                if not map_mask.overlap(self.mask, temp_offset):
                    self.y = temp_y
                    self.rect = temp_rect
                    return rasbr
        return rasbr

    def draw(self, surface, camera):
        draw_rect = self.rect.move(camera.offset_x, camera.offset_y)
        surface.blit(self.image, draw_rect.topleft)

    def get_st_end(self):
        barrel_length = 20
        end_x = self.x + math.sin(math.radians(self.angle)) * barrel_length
        end_y = self.y - math.cos(math.radians(self.angle)) * barrel_length
        return end_x, end_y
