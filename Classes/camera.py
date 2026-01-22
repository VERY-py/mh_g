from setting import *

class Camera:
    def __init__(self, target):
        self.target = target
        self.offset_x = 0
        self.offset_y = 0

    def update(self):
        self.offset_x = SCREEN_WIDTH // 2 - int(self.target.x)
        self.offset_y = SCREEN_HEIGHT // 2 - int(self.target.y)

    def apply(self, rect):
        return pygame.Rect(rect.x + self.offset_x, rect.y + self.offset_y, rect.width, rect.height)