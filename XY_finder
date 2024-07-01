import pyautogui
import keyboard
import time

print("Нажмите 'P' для получения координат, нажмите 'Q' для выхода.")

def get_coordinates():
    while True:
        if keyboard.is_pressed('P'):
            x, y = pyautogui.position()
            print(f"Координаты: ({x}, {y})")
            time.sleep(1)  # Задержка, чтобы предотвратить многократное считывание координат при одном нажатии
        if keyboard.is_pressed('Q'):
            print("Выход")
            break

if __name__ == "__main__":
    get_coordinates()
