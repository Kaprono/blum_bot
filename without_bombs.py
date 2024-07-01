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

# Координаты рабочего окна
WORK_WINDOW = {
    'left': 681,
    'top': 257,
    'right': 1231,
    'bottom': 911,
}

# Координаты кнопки "Play"
PLAY_BUTTON_COORDS = (971, 866)

print("\nРабочее окно задано\nНажмите 'S' для старта.")

paused = True
last_check_time = time.time()
last_play_click_time = time.time()

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
    pixel_found = False
    if pixel_found == True:
        break

    for x in range(0, width, 20):
        for y in range(0, height, 20):
            r, g, b = scrn.getpixel((x, y))
            if (b in range(0, 125)) and (r in range(102, 220)) and (g in range(200, 255)):
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

    # Нажать кнопку "Play" не чаще чем раз в 7 секунд
    if not pixel_found and current_time - last_play_click_time >= 7:
        click(*PLAY_BUTTON_COORDS)
        print('Кнопка "Play" нажата')
        last_play_click_time = current_time
        time.sleep(1)

print('Стоп')
