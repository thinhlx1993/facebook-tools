import os
import time
import pyautogui
import logging
from datetime import datetime
import clipboard


os.makedirs('uploaded', exist_ok=True)
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


def click_to(btn, region=None, waiting_time=1000):
    logger.info(f"Click to {btn}")
    start_count = 0

    while start_count < waiting_time:
        ret = pyautogui.locateOnScreen(f"btn/{btn}", confidence=.8, region=region)
        start_count += 1
        if ret:
            pyautogui.click(ret, interval=0.5)
            break
        time.sleep(0.1)


def click_many(btn, region=None):
    logger.info(f"Click many {btn}")
    results = pyautogui.locateAllOnScreen(f"btn/{btn}", confidence=.8, region=region)
    for ret in results:
        pyautogui.click(ret, interval=0.5)
    return len(list(results))


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


if __name__ == '__main__':
    number_invited = 0
    while number_invited < 200:
        if check_exist("like.PNG", region=(1050, 200, 70, 800)):
            click_to("like.PNG", region=(1050, 200, 70, 800))

            waiting = 0
            while waiting <= 3:
                number_invited += click_many("invite.PNG", region=(1050, 200, 600, 800))
                pyautogui.moveTo(x=1091, y=573, duration=0.5)
                pyautogui.scroll(-400)
                pyautogui.scroll(-400)
                time.sleep(1)
                if not check_exist("invite.PNG", region=(1050, 200, 600, 800)):
                    waiting += 1
            if check_exist("close_invite.PNG", region=(1050, 200, 600, 800)):
                click_to("close_invite.PNG", region=(1050, 200, 600, 800))
        pyautogui.moveTo(x=1635, y=655, duration=0.5)
        pyautogui.click(x=1635, y=655)
        pyautogui.scroll(-1500)
        pyautogui.scroll(-1000)
        time.sleep(1)
