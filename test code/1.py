import serial
import pygame
from pygame.locals import *
import configparser
import platform
import random
import math

# 初始化串口通信
system = platform.system()
print(system)
if system == 'Windows':

    ser = serial.Serial('COM7', 115200)    
else:
    ser = serial.Serial('/dev/ttyUSB0', 115200) 
ser.flushInput()

# 初始化Pygame
pygame.init()

# 获取当前显示设备信息
info = pygame.display.Info()
# 获取当前分辨率
resolution = (info.current_w, info.current_h)
print("Current resolution : ", resolution)


screen = pygame.display.set_mode((300, 420))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()




# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 获取颜色配置
colors = {}
for key, value in config['colors'].items():
    if key == 'PIC':
        colors[key] = int(value)
    else:
        colors[key] = tuple(map(int, value.split(',')))

first_color_key, first_color_value = next(iter(colors.items()))
print(first_color_key, first_color_value)


current_color = first_color_key  # 默认config的第一個顏色

# 图片路径
image_base_path = "pattern/pic"  # 图片基础路径
current_pic_index = 1  # 当前图片编号






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
# 创建 MovingSquare 实例
WIDTH, HEIGHT = 800, 600
moving_square = MovingSquare(info.current_w, info.current_h)

# 主循环
running = True
while running:
    # 接收串口数据
    try:
        if ser.in_waiting > 0:
            cmd = ser.read(2)
            
            if cmd[0]==0xF1:
                color_index = int(cmd[1])+1
                print("received:",cmd)
                if 1 <= color_index <= len(colors):
                    current_color = list(colors.keys())[color_index - 1]
            else:
                print("skip rx",ser.in_waiting)

    except Exception as e:
        print("Error:", e)  # 打印错误信息
        continue  # 继续下一次循环

    # 处理事件
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_q:
                running = False
        elif event.type == MOUSEBUTTONDOWN:
            # 切换颜色
            color_keys = list(colors.keys())
            current_color_index = color_keys.index(current_color)
            next_color_index = (current_color_index + 1) % len(colors)
            current_color = color_keys[next_color_index]

    # 绘制屏幕
    if current_color in colors:
        
        if current_color.startswith("pic"):
            # 图片路径
            image_path = f"{image_base_path}{current_pic_index}.jpg"  # 构建图片路径
            # 加载图片
            try:
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (screen.get_width(), screen.get_height()))
            except pygame.error as e:
                print(f"Error loading image: {e}")
                
            
            screen.blit(image, (0, 0))  # 显示图片
        elif current_color.startswith("square"):
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            
            # 更新方块位置
            moving_square.update()

            # 填充背景色
            screen.fill(BLACK)

            # 绘制方块
            moving_square.draw(screen)
        else:
            screen.fill(colors[current_color])
    pygame.display.flip()

    clock.tick(30)

# 清理
pygame.quit()
ser.close()
