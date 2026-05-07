import subprocess
import time

import cv2
import easyocr
import mss
import numpy as np
import pyautogui


CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

reader = easyocr.Reader(["pt", "en"])


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


def search_petrolina():

    bbox = find_text("Pesquise no Google Maps")

    if not bbox:
        return

    pyautogui.write("Petrolina", interval=0.05)

    pyautogui.press("enter")


def main():

    open_chrome()

    open_google_maps()

    search_petrolina()


if __name__ == "__main__":
    main()
