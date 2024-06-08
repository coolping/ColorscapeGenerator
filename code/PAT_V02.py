import serial
import pygame
from pygame.locals import *
import configparser
import platform
import random
import math
import re

# init serial comport
system = platform.system()
print(system)
if system == 'Windows':

    ser = serial.Serial('COM11', 115200)    
else:
    ser = serial.Serial('/dev/ttyUSB0', 921600) 
    #ser = serial.Serial('/dev/ttyAMA10', baudrate=115200,timeout=1) #ttyAMA10 is DebugPort
ser.flushInput()


# Pygame 
pygame.init()

pygame.mouse.set_visible(False)

info = pygame.display.Info()

resolution = (info.current_w, info.current_h)
print("Current resolution : ", resolution)


#screen = pygame.display.set_mode((300, 420))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

clock = pygame.time.Clock()

# read ini
config = configparser.ConfigParser()
config.read('config.ini')

# Fetch color setting
colors = {}
for key, value in config['colors'].items():
    if key == 'PIC':
        colors[key] = int(value)
    else:
        colors[key] = tuple(map(int, value.split(',')))

first_color_key, first_color_value = next(iter(colors.items()))
print("Default color =",first_color_key, first_color_value)

current_color = first_color_key  # default config color setup

# Pattern generation path
image_base_path = "pattern/pic"  
current_pic_index = 1  # pic index


# Square color define
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class MovingSquare:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.square_size = 200
        self.square_x = random.randint(0, self.width - self.square_size)
        self.square_y = random.randint(0, self.height - self.square_size)
        self.speed = random.uniform(10, 15)
        self.angle = random.uniform(0, 2 * math.pi)

    def update(self):
        self.square_x += self.speed * math.cos(self.angle)
        self.square_y += self.speed * math.sin(self.angle)

        if self.square_x <= 0 or self.square_x >= self.width - self.square_size:
            self.angle = math.pi - self.angle
        if self.square_y <= 0 or self.square_y >= self.height - self.square_size:
            self.angle = -self.angle

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.square_x, self.square_y, self.square_size, self.square_size))
# Create MovingSquare class
moving_square = MovingSquare(info.current_w, info.current_h)

running = True
pattern_target = re.compile(r'Pattern_Change = (\d+)')


while running:
    # check serial data
    try:
        if ser.in_waiting > 0:
            #cmd = ser.read(2)
            cmd = ser.readline().decode('ascii').strip()
            
            # 嘗試匹配 Pattern_Change 格式的數據
            match = pattern_target.match(cmd)           
            color_index = int(match.group(1))
            print("received:",cmd)
            if 1 <= color_index <= len(colors):
                current_color = list(colors.keys())[color_index - 1]
    except Exception as e:
        print("Error:", e)  
        continue

    # Event handle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("QUIT")
            #running = False                
        elif event.type == pygame.KEYDOWN:
            if event.key == K_q:
                print("KEYDOWN")
                running = False
            elif event.key == pygame.K_UP:
                # press up key for Change color increase 
                color_keys = list(colors.keys())
                current_color_index = color_keys.index(current_color)
                next_color_index = (current_color_index + 1) % len(colors)
                current_color = color_keys[next_color_index]
            elif event.key == pygame.K_DOWN:
                # press down key for Change color decrease
                color_keys = list(colors.keys())
                current_color_index = color_keys.index(current_color)
                next_color_index = (current_color_index - 1) % len(colors)
                current_color = color_keys[next_color_index]
        #elif event.type == MOUSEBUTTONDOWN:
         #   print("MOUSEBUTTONDOWN_Change color")
            # click mouse lfet key for Change color increase


    # draw the picture
    if current_color in colors:
        
        if current_color.startswith("pic"):
            current_pic_index = current_color[3]

            image_path = f"{image_base_path}{current_pic_index}.jpg" 
            
            try:
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (screen.get_width(), screen.get_height()))
            except pygame.error as e:
                print(f"Error loading image: {e}")
                
            
            screen.blit(image, (0, 0))  # show the picture
        elif current_color.startswith("square"):
            #screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            
            # update the square position
            moving_square.update()

            # fill the background
            screen.fill(BLACK)

            #  draw the square
            moving_square.draw(screen)
        else:
            screen.fill(colors[current_color])
    pygame.display.flip()

    clock.tick(60)
print("close")
pygame.quit()
ser.close()






