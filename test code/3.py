import pygame
import sys
from datetime import datetime

# 初始化Pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw Date and Time")

# 设置字体
font = pygame.font.Font(None, 36)  # 使用默认字体和大小，也可以指定字体文件路径和字体大小

# 主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 获取当前日期和时间并格式化为指定格式
    current_datetime = "DQA_TEST "+datetime.now().strftime("%Y%m%d%H%M%S")

    # 渲染文本
    text_surface = font.render(current_datetime, True, (255, 255, 255))  # 白色

    # 获取文本所占的矩形区域
    text_rect = text_surface.get_rect()

    # 设置文本位置为窗口中心
    text_rect.center = (WIDTH // 2, HEIGHT // 2)

    # 清空屏幕
    screen.fill((0, 0, 0))  # 填充黑色背景

    # 在屏幕上绘制文本
    screen.blit(text_surface, text_rect)

    # 更新屏幕
    pygame.display.flip()

# 退出Pygame
pygame.quit()
sys.exit()
