import pygame
import random
import math

# 初始化Pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class MovingSquare:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.square_size = 50
        self.square_x = random.randint(0, self.width - self.square_size)
        self.square_y = random.randint(0, self.height - self.square_size)
        self.speed = random.uniform(10, 15)
        self.angle = random.uniform(0, 2 * math.pi)

    def update(self):
        self.square_x += self.speed * math.cos(self.angle)
        self.square_y += self.speed * math.sin(self.angle)

        # 碰撞检测
        if self.square_x <= 0 or self.square_x >= self.width - self.square_size:
            self.angle = math.pi - self.angle
        if self.square_y <= 0 or self.square_y >= self.height - self.square_size:
            self.angle = -self.angle

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.square_x, self.square_y, self.square_size, self.square_size))

# 设置窗口大小和标题
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Square Animation")

# 创建 MovingSquare 实例
moving_square = MovingSquare(WIDTH, HEIGHT)

# 主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新方块位置
    moving_square.update()

    # 填充背景色
    screen.fill(BLACK)

    # 绘制方块
    moving_square.draw(screen)

    # 更新屏幕
    pygame.display.flip()

    # 控制帧率
    pygame.time.Clock().tick(30)

# 退出Pygame
pygame.quit()
