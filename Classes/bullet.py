from setting import *

class Bullet:
    def __init__(self, x, y, angle, speed, rasbr, is_knife):
        self.x = x
        self.y = y
        self.R = random.randint(-abs(rasbr), abs(rasbr))
        self.angle = angle
        self.speed = speed
        self.knf = 0
        self.is_knife = is_knife
        self.radius = BULLET_RADIUS
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                self.radius * 2, self.radius * 2)

    def update(self, map_mask):

        dx = math.sin(math.radians(self.angle+self.R)) * self.speed
        dy = -math.cos(math.radians(self.angle+self.R)) * self.speed

        steps = 5
        step_x = dx / steps
        step_y = dy / steps

        collided = False
        if self.is_knife:
            self.knf += 1
            if map_mask.get_at(self.rect.center) != 0 or self.knf >= 2:
                collided = True
        else:
            for _ in range(steps):
                self.x += step_x
                self.y += step_y
                self.rect.center = (int(self.x), int(self.y))

                if map_mask.get_at(self.rect.center) != 0:
                    collided = True
                    break
        return collided

    def draw(self, surface, camera):
        screen_pos = (int(self.x + camera.offset_x), int(self.y + camera.offset_y))
        if self.is_knife: pygame.draw.circle(surface, ORANGE, screen_pos, 30)
        else: pygame.draw.circle(surface, ORANGE, screen_pos, self.radius)

