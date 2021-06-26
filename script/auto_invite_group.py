import os
import time
import pyautogui
import logging
import clipboard
from datetime import datetime
from utils import logger, click_to, click_many, check_exist, waiting_for


if __name__ == '__main__':
    number_invited = 0
    click_to("start_invite_group.PNG")
    while True:
        waiting_for("check_box.PNG")
        number_check_box = click_many("check_box.PNG", confidence=1)
        number_invited += number_check_box
        print(f"number invited: {number_invited}")
        pyautogui.moveTo(1035, 751)
        pyautogui.scroll(-700)
        if number_invited > 300:
            break
    click_to("send_invite_group.PNG")