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

# Координаты рабочего окна
WORK_WINDOW = {
    'left': 13,
    'top': 91,
    'right': 2505,
    'bottom': 1033
}

# Координаты кнопки "Новая игра"
NEW_GAME_BUTTON_COORDS = (1500, 800)  # Замените на реальные координаты кнопки "Новая игра"

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
        click(NEW_GAME_BUTTON_COORDS[0], NEW_GAME_BUTTON_COORDS[1])
        last_check_time = current_time

    if current_time - last_object_time >= 3:
        click(NEW_GAME_BUTTON_COORDS[0], NEW_GAME_BUTTON_COORDS[1])
        last_object_time = time.time()

print('Стоп')
