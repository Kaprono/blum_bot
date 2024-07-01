import pyautogui
import time
import keyboard
import random
from pynput.mouse import Button, Controller
import pygetwindow as gw
import tkinter as tk
from tkinter import simpledialog
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
            logging.info('Начало новой игры')
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

# Функция для проверки белого цвета на кнопке Play
def check_play_button(scrn, window_rect):
    width, height = scrn.size
    for x in range(0, width, 20):
        for y in range(height - height // 7, height, 20):
            r, g, b = scrn.getpixel((x, y))
            if (r, g, b) == (255, 255, 255):
                screen_x = window_rect[0] + x
                screen_y = window_rect[1] + y
                click(screen_x, screen_y)
                logging.info('Нажата кнопка Play')
                time.sleep(0.001)
                return True
    return False

# Функция для проверки наличия бомбы на экране
def check_for_bombs(scrn):
    width, height = scrn.size
    for x in range(0, width, 10):
        for y in range(130, height, 10):
            r, g, b = scrn.getpixel((x, y))
            if g == b and g in range(100, 150):  # Проверка на серый цвет
                logging.info(f'Обнаружена бомба по координатам: ({x}, {y}), пауза')
                return True
    return False

# Функция для проверки наличия бомбы вокруг координат звезды
def check_bomb_around_star(scrn, x, y):
    radius = 20  # Увеличен радиус проверки вокруг звезды
    for i in range(-radius, radius, 5):
        for j in range(-radius, radius, 5):
            if 0 <= x + i < scrn.width and 0 <= y + j < scrn.height:
                r, g, b = scrn.getpixel((x + i, y + j))
                if g == b and g in range(100, 150):  # Проверка на серый цвет
                    logging.info(f'Обнаружена бомба рядом со звездой по координатам: ({x + i}, {y + j}), пропуск клика')
                    return True
    return False

# Координаты рабочего окна
WORK_WINDOW = {
    'left': 1074,
    'top': 214,
    'right': 1468,
    'bottom': 880
}

logging.info("\nРабочее окно задано\nНажмите 'S' для старта.")

paused = True
last_check_time = time.time()
last_blue_check_time = time.time()
last_pause_time = time.time()

while True:
    try:
        if keyboard.is_pressed('S') and time.time() - last_pause_time > 0.1:
            paused = not paused
            last_pause_time = time.time()
            if paused:
                logging.info('Пауза')
            else:
                logging.info('Работаю')
                logging.info("Для паузы нажми 'S'")
            time.sleep(0.2)

        window_rect = (
            WORK_WINDOW['left'], WORK_WINDOW['top'], WORK_WINDOW['right'] - WORK_WINDOW['left'], WORK_WINDOW['bottom'] - WORK_WINDOW['top']
        )

        scrn = pyautogui.screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))

        if not paused:
            width, height = scrn.size
            pixel_found = False

            if check_for_bombs(scrn):
                time.sleep(1.3)  # Пауза при обнаружении бомбы
                continue

            for x in range(0, width, 10):  # Шаг проверки пикселей
                for y in range(130, height, 10):  # Шаг проверки пикселей
                    r, g, b = scrn.getpixel((x, y))
                    if (b in range(0, 125)) and (r in range(102, 220)) and (g in range(200, 255)):
                        # Проверка наличия бомбы вокруг звезды
                        if check_bomb_around_star(scrn, x, y):
                            continue
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

            if check_play_button(scrn, window_rect):
                logging.info('Кнопка Play найдена и нажата')
                time.sleep(0.5)
                continue

            next_check_time = random.uniform(1.5, 2.50)

            if current_time - last_pause_time >= next_check_time:
                pause_time = random.uniform(0.60, 1.10)
                time.sleep(pause_time)
                last_pause_time = current_time

            if current_time - last_blue_check_time >= 0.1:
                if check_blue_color(scrn, window_rect):
                    last_blue_check_time = current_time

    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
        time.sleep(1)

logging.info('Стоп')
