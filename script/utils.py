import pyautogui
import logging
import time
import random


# create logger with 'spam_application'
logger = logging.getLogger('application')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('app.log')
fh.setLevel(logging.INFO)
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
    return random.uniform(0, 1)


def click_to(btn, region=None, waiting_time=1000):
    logger.info(f"Click to {btn}")
    start_count = 0

    while start_count < waiting_time:
        ret = pyautogui.locateOnScreen(f"btn/{btn}", confidence=.8, region=region)
        start_count += 1
        if ret:
            pyautogui.click(ret, interval=random_interval())
            break
        time.sleep(0.2)


def click_many(btn, region=None):
    logger.info(f"Click many {btn}")
    elements = pyautogui.locateAllOnScreen(f"btn/{btn}", confidence=.8, region=region)
    number_element = len(list(pyautogui.locateAllOnScreen(f"btn/{btn}", confidence=.8, region=region)))
    for ret in elements:
        pyautogui.click(ret, interval=random_interval())
    return number_element


def check_exist(btn, region=None):
    exist = pyautogui.locateOnScreen(f"btn/{btn}", confidence=.8, region=region)
    logger.info(f"Check exist {btn} result {exist}")
    return exist


def waiting_for(btn, region=None):
    logger.info(f"Watiing for {btn}")
    while True:
        ret = pyautogui.locateCenterOnScreen(f"btn/{btn}", confidence=.8, region=region)
        if ret:
            x, y = ret
            return x, y
