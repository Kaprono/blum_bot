import pyautogui
import time
import keyboard
import random
from pynput.mouse import Button, Controller
import pygetwindow as gw
import tkinter as tk
from tkinter import simpledialog

mouse = Controller()
time.sleep(0.5)

# Функция для клика по указанным координатам с небольшой случайной поправкой
def click(xs, ys):
    mouse.position = (xs, ys + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)

# Функция для выбора окна с помощью GUI
def choose_window_gui():
    root = tk.Tk()
    root.withdraw()

    windows = gw.getAllTitles()
    if not windows:
        return None

    choice = simpledialog.askstring("Выбор окна Telegram", "Введите номер окна:\n" + "\n".join(
        f"{i}: {window}" for i, window in enumerate(windows)))

    if choice is None or not choice.isdigit():
        return None

    choice = int(choice)
    if 0 <= choice < len(windows):
        return windows[choice]
    else:
        return None

# Функция для проверки белого цвета в нижней части экрана для старта новой игры
def check_white_color(scrnb, window_rectb):
    widthb, heightb = scrnb.size
    for xb in range(0, widthb, 20):
        yb = heightb - heightb // 7
        rb, gb, bb = scrnb.getpixel((xb, yb))
        if (rb, gb, bb) == (255, 255, 255):
            screen_xb = window_rectb[0] + xb
            screen_yb = window_rectb[1] + yb
            click(screen_xb, screen_yb)
            print('Начинаю новую игру')
            time.sleep(0.001)
            return True
    return False

# Функция для проверки синего цвета
def check_blue_color(scrnq, window_rectq):
    widthq, heightq = scrnq.size
    for xq in range(0, widthq, 20):
        for yq in range(200, heightq, 20):
            rq, gq, bq = scrnq.getpixel((xq, yq))
            if (rq in range(0, 180)) and (gq in range(102, 250)) and (bq in range(200, 255)):
                screen_xq = window_rectq[0] + xq
                screen_yq = window_rectq[1] + yq
                click(screen_xq, screen_yq)
                return True
    return False

# Координаты рабочего окна
WORK_WINDOW = {
    'left': 1074,
    'top': 214,
    'right': 1468,
    'bottom': 895
}

# Координаты кнопки "Play"
PLAY_BUTTON_COORDS = (1420, 706)

print("\nРабочее окно задано\nНажмите 'S' для старта.")

paused = True
last_check_time = time.time()
last_blue_check_time = time.time()
last_pause_time = time.time()

while True:
    if keyboard.is_pressed('S') and time.time() - last_pause_time > 0.1:
        paused = not paused
        last_pause_time = time.time()
        if paused:
            print('Пауза')
        else:
            print('Работаю')
            print(f"Для паузы нажми 'S'")
        time.sleep(0.2)

    window_rect = (
        WORK_WINDOW['left'], WORK_WINDOW['top'], WORK_WINDOW['right'] - WORK_WINDOW['left'], WORK_WINDOW['bottom'] - WORK_WINDOW['top']
    )

    scrn = pyautogui.screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))

    if not paused:
        width, height = scrn.size
        pixel_found = False

        for x in range(0, width, 20):
            for y in range(130, height, 20):
                r, g, b = scrn.getpixel((x, y))
                if (b in range(0, 125)) and (r in range(102, 220)) и (g в диапазоне (200, 255)):
                    screen_x = window_rect[0] + x + 3
                    screen_y = window_rect[1] + y + 5
                    click(screen_x, screen_y)
                    time.sleep(0.002)
                    pixel_found = True
                    break

        current_time = time.time()
        if current_time - last_check_time >= 10:
            if check_white_color(scrn, window_rect):
                last_check_time = current_time

        next_check_time = random.uniform(1.5, 2.50)

        if current_time - last_pause_time >= next_check_time:
            pause_time = random.uniform(0.60, 1.10)
            time.sleep(pause_time)
            last_pause_time = current_time

        if current_time - last_blue_check_time >= 0.1:
            if check_blue_color(scrn, window_rect):
                last_blue_check_time = current_time

        # После окончания игрового процесса нажать кнопку "Play"
        if not pixel_found:
            click(*PLAY_BUTTON_COORDS)
            print('Кнопка "Play" нажата')
            time.sleep(1)

print('Стоп')
