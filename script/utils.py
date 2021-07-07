import clipboard
import pyautogui
import logging
import time
import random


# create logger with 'spam_application'
logger = logging.getLogger('application')
# logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('app.log')
# fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


def random_interval():
    return random.uniform(0, 0.5)


def click_to(btn, region=None, waiting_time=1000):
    print(f"Click to {btn}")
    start_count = 0

    while start_count < waiting_time:
        ret = pyautogui.locateOnScreen(f"btn/{btn}", confidence=.8, region=region)
        start_count += 1
        if ret:
            pyautogui.click(ret, interval=random_interval())
            break
        time.sleep(0.2)


def click_many(btn, region=None, confidence=0.8):
    print(f"Click many {btn}")
    elements = pyautogui.locateAllOnScreen(f"btn/{btn}", confidence=confidence, region=region)
    number_element = len(list(pyautogui.locateAllOnScreen(f"btn/{btn}", confidence=confidence, region=region)))
    for ret in elements:
        pyautogui.click(ret, interval=random_interval(), duration=0.1)
    return number_element


def check_exist(btn, region=None):
    exist = pyautogui.locateOnScreen(f"btn/{btn}", confidence=.8, region=region)
    print(f"Check exist {btn} result {exist}")
    return exist


def waiting_for(btn, region=None, confidence=.8, waiting_time=100):
    print(f"Watiing for {btn}")
    start_count = 0
    while start_count < waiting_time:
        start_count += 1
        ret = pyautogui.locateCenterOnScreen(f"btn/{btn}", confidence=confidence, region=region)
        if ret:
            return ret
    return None


def paste_text(inp_text):
    clipboard.copy(inp_text)
    pyautogui.hotkey('ctrl', 'v', interval=0.2)


def get_title():
    with open("title.txt") as file:
        lines = [line.strip() for line in file.readlines() if line.strip() != ""]
        title = random.choice(lines)
        logger.info(title)
        return title