import pyautogui
import time
import keyboard
import random
from pynput.mouse import Button, Controller

mouse = Controller()
time.sleep(0.5)

def click(x, y):
    mouse.position = (x, y + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)

def check_white_color(scrn, window_rect):
    width, height = scrn.size
    for x in range(0, width, 20):
        y = height - height // 8
        r, g, b = scrn.getpixel((x, y))
        if (r, g, b) == (255, 255, 255):
            screen_x = window_rect[0] + x
            screen_y = window_rect[1] + y
            click(screen_x, screen_y)
            print('Начинаю новую игру')
            time.sleep(0.001)
            return True
    return False

def check_for_objects(scrn, window_rect):
    width, height = scrn.size
    for x in range(0, width, 20):
        for y in range(0, height, 20):
            r, g, b = scrn.getpixel((x, y))
            if (r in range(200, 255)) and (g in range(0, 200)) and (b in range(200, 255)):  # Фиолетовые объекты
                screen_x = window_rect[0] + x + 3
                screen_y = window_rect[1] + y + 5
                click(screen_x, screen_y)
                return True
            elif (r in range(128, 200)) and (g in range(128, 200)) and (b in range(128, 200)):  # Серые объекты
                screen_x = window_rect[0] + x + 3
                screen_y = window_rect[1] + y + 5
                click(screen_x, screen_y)
                return True
    return False

# Координаты рабочего окна (каждый меняет под себя черех XY_finder.py)
WORK_WINDOW = {
    'left': 1003,
    'top': 322,
    'right': 1549,
    'bottom': 914
}

print("\nРабочее окно задано\nНажмите 'S' для старта.")

paused = True
last_check_time = time.time()
last_object_time = time.time()

while True:
    if keyboard.is_pressed('S'):
        paused = not paused
        if paused:
            print('Пауза')
        else:
            print('Работаю')
            print(f"Для паузы нажми 'S'")
        time.sleep(0.2)

    if paused:
        continue

    window_rect = (
        WORK_WINDOW['left'], WORK_WINDOW['top'], WORK_WINDOW['right'] - WORK_WINDOW['left'], WORK_WINDOW['bottom'] - WORK_WINDOW['top']
    )

    scrn = pyautogui.screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))

    width, height = scrn.size

    if check_for_objects(scrn, window_rect):
        last_object_time = time.time()

    current_time = time.time()
    if current_time - last_check_time >= 10:
        if check_white_color(scrn, window_rect):
            last_check_time = current_time

    if current_time - last_object_time >= 3:
        click(1420, 706)  # Нажатие кнопки Play
        last_object_time = time.time()

print('Стоп')
