from tkinter import *
from PIL import Image, ImageTk

# 初始颜色为白色
current_color = (255, 255, 255)

# 创建主窗口
root = Tk()
root.title("Color Switcher")

# 隐藏窗口边框和标题栏，并设置全屏
root.attributes('-fullscreen', True)
root.overrideredirect(True)
root.config(bg="red")  # 设置窗口背景颜色为红色

# 创建画布
canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg="white")
canvas.pack()

# 更新画布颜色
def update_color():
    global current_color
    canvas.configure(bg="#%02x%02x%02x" % current_color)

# 切换颜色
def switch_color(event):
    global current_color
    if current_color == (255, 255, 255):
        current_color = (255, 0, 0)  # 红色
    elif current_color == (255, 0, 0):
        current_color = (0, 255, 0)  # 绿色
    else:
        current_color = (0, 0, 255)  # 蓝色
    update_color()

# 退出应用程序
def exit_app(event):
    if event.char.lower() == 'q':
        root.destroy()

# 绑定按键事件
root.bind("<KeyPress>", switch_color)
root.bind("<KeyPress>", exit_app)

# 更新初始颜色
update_color()

# 运行程序
root.mainloop()
