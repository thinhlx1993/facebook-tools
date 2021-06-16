import os
import time
import pyautogui
import logging
import clipboard
from datetime import datetime
from utils import logger, click_to, click_many, check_exist, waiting_for


if __name__ == '__main__':
    number_invited = 0
    while True:
        click_to("start_invite_group.PNG")
        waiting_for("check_box.PNG")
        number_check_box = click_many("check_box.PNG")
        number_invited += number_check_box
        click_to("send_invite_group.PNG")
        print(f"number invited: {number_invited}")
