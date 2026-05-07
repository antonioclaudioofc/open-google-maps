import subprocess
import threading
import time
import tkinter as tk

import cv2
import easyocr
import keyboard
import mss
import numpy as np
import pyautogui

import shutil


def get_chrome_path():

    possible_paths = [
        shutil.which("chrome"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]

    for path in possible_paths:
        if path:
            return path

    return None


CHROME_PATH = get_chrome_path()
pyautogui.FAILSAFE = True

reader = easyocr.Reader(["pt", "en"])

running = False


def screenshot():

    with mss.MSS() as sct:
        monitor = sct.monitors[1]

        img = np.array(sct.grab(monitor))

        return img


def preprocess(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    upscale = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    contrast = cv2.equalizeHist(upscale)

    thresh = cv2.threshold(contrast, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    return thresh


def find_text(target):

    image = screenshot()

    processed = preprocess(image)

    results = reader.readtext(processed, detail=1)

    for result in results:
        bbox, text, confidence = result

        if target.lower() in text.lower():
            return bbox

    return None


def click_bbox_center(bbox):

    x = int((bbox[0][0] + bbox[2][0]) / 2)

    y = int((bbox[0][1] + bbox[2][1]) / 2)

    x = int(x / 2)
    y = int(y / 2)

    pyautogui.moveTo(x, y, duration=0.3)

    pyautogui.click(x, y)


def wait(seconds=2):
    time.sleep(seconds)


def open_chrome():

    subprocess.Popen(CHROME_PATH)

    wait(3)


def open_google_maps():

    pyautogui.hotkey("ctrl", "t")

    wait(1)

    pyautogui.write("https://maps.google.com", interval=0.03)

    pyautogui.press("enter")

    wait(6)


def wait_for_text(target, timeout=15):

    start = time.time()

    while time.time() - start < timeout:
        bbox = find_text(target)

        if bbox:
            return bbox

        time.sleep(1)

    return None


def search_petrolina():

    bbox = wait_for_text("Pesquise no Google Maps")

    if not bbox:
        print("Campo não encontrado")

        return

    click_bbox_center(bbox)

    wait(1)

    pyautogui.write("Petrolina", interval=0.1)

    pyautogui.press("enter")


def run_agent():

    global running

    running = True

    update_status("Rodando")

    try:
        if not running:
            return

        open_chrome()

        if not running:
            return

        open_google_maps()

        if not running:
            return

        search_petrolina()

        update_status("Finalizado")

    except Exception as e:
        update_status("Erro")

        print(e)

    running = False


def start_agent():

    global running

    if running:
        return

    thread = threading.Thread(target=run_agent, daemon=True)

    thread.start()


def stop_agent():

    global running

    running = False

    update_status("Parado")


def update_status(text):

    status_label.config(text=f"Status: {text}")


keyboard.add_hotkey("ctrl+alt+s", start_agent)

keyboard.add_hotkey("ctrl+alt+x", stop_agent)


root = tk.Tk()

root.title("Google Maps Agent")

root.geometry("350x350")

root.resizable(False, False)

title = tk.Label(root, text="Google Maps Agent", font=("Arial", 18, "bold"))

title.pack(pady=20)


status_label = tk.Label(root, text="Status: Parado", font=("Arial", 12))

status_label.pack(pady=10)


start_button = tk.Button(
    root,
    text="Iniciar",
    width=20,
    height=2,
    bg="green",
    fg="white",
    command=start_agent,
)

start_button.pack(pady=10)


stop_button = tk.Button(
    root, text="Parar", width=20, height=2, bg="red", fg="white", command=stop_agent
)

stop_button.pack(pady=10)


info_label = tk.Label(
    root, text=("CTRL + ALT + S → iniciar\nCTRL + ALT + X → parar"), font=("Arial", 9)
)

info_label.pack(pady=15)


root.mainloop()
