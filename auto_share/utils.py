import clipboard
import requests
import logging
import pymongo
import pyautogui
import time
import random
import pyotp
import uuid
import re
from bs4 import BeautifulSoup
from bson import ObjectId


# create logger with 'spam_application'
logger = logging.getLogger('application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('app.log')
# fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
# ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


client = pymongo.MongoClient("mongodb+srv://facebook:auft.baff1vawn*WEC@cluster0.dtlfk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test
phone_table = db['phone']
email_table = db['emails']
cookies_table = db['cookies']
via_share_table = db['via_share']
scheduler_table = db['scheduler']


def random_interval():
    return random.uniform(0.5, 2)


def click_to(btn, confidence=0.8, region=None, waiting_time=1000, interval=None, check_close=True, duration=1):
    logger.debug(f"Click to {btn}")
    start_count = 0
    while start_count < waiting_time:
        ret = pyautogui.locateCenterOnScreen(f"btn/{btn}", confidence=confidence, region=region)
        start_count += 1
        if ret:
            btn_x, btn_y = ret
            pyautogui.moveTo(btn_x, btn_y, duration=duration)
            interval = random_interval() if interval is None else interval
            pyautogui.click(btn_x, btn_y, interval=interval, duration=duration)
            break

        time.sleep(0.2)


def click_many(btn, region=None, confidence=0.8, log=True, duration=1):
    if log:
        logger.debug(f"Click many {btn}")
    elements = pyautogui.locateAllOnScreen(f"btn/{btn}", confidence=confidence, region=region)
    number_element = len(list(pyautogui.locateAllOnScreen(f"btn/{btn}", confidence=confidence, region=region)))
    for ret in elements:
        pyautogui.moveTo(ret, duration=duration)
        pyautogui.click(ret, interval=random_interval(), duration=duration)
    return number_element


def check_exist(btn, region=None, confidence=0.8):
    exist = pyautogui.locateOnScreen(f"btn/{btn}", confidence=confidence, region=region)
    logger.debug(f"Check exist {btn} result {exist}")
    return exist


def waiting_for(btn, region=None, confidence=0.8, waiting_time=1000):
    logger.debug(f"Waiting for {btn}")
    start_count = 0
    while start_count < waiting_time:
        start_count += 1
        ret = pyautogui.locateCenterOnScreen(f"btn/{btn}", confidence=confidence, region=region)
        if ret:
            x, y = ret
            return x, y

        time.sleep(0.2)
    return None


def deciscion(btns, region=None, confidence=0.8):
    while True:
        logger.debug(f"Waiting for {btns}")
        for btn_index, btn in enumerate(btns):
            ret = pyautogui.locateCenterOnScreen(f"btn/{btn}", confidence=confidence, region=region)
            if ret:
                x, y = ret
                return x, y, btn_index


def typeing_text(inp_text):
    pyautogui.typewrite(inp_text, interval=0.2)


def paste_text(inp_text):
    clipboard.copy(inp_text)
    pyautogui.hotkey('ctrl', 'v', interval=0.2)


def get_title():
    with open("title.txt") as file:
        lines = [line.strip() for line in file.readlines() if line.strip() != ""]
        return random.choice(lines)


def relative_position(x, y):
    default_width = 1920
    default_height = 1080
    ratio_x = x/default_width
    ratio_y = y/default_height
    width, height = pyautogui.size()
    return int(ratio_x*width), int(ratio_y*height)
