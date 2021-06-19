import random
import time

import pyautogui
from datetime import datetime
from utils import click_to, click_many, check_exist, paste_text, typeing_text, waiting_for, deciscion, \
    relative_position, get_title, scheduler_table


if __name__ == '__main__':
    while True:
        time.sleep(60)
        scheduler = scheduler_table.find_one({"shared": False, "scheduler_time": {"$lte": datetime.now().timestamp()}})
        if scheduler:
            scheduler_table.update_one({"_id": scheduler['_id']}, {"$set": {"shared": True}})
            video_id = scheduler['video_id']
            print(f"share video {video_id}")
            time.sleep(2)
            pyautogui.hotkey('winleft', 'd')
            time.sleep(2)
            browsers = pyautogui.locateAllOnScreen(f"btn/coccoc.PNG", confidence=0.9, region=(0, 1040, 1920, 40))
            for browser in browsers:
                pyautogui.click(browser)
                click_to("dark_logo.PNG", confidence=0.8)
                pyautogui.click(relative_position(200, 54))
                paste_text(f"fb.com/{video_id}")
                pyautogui.hotkey('enter')
                time.sleep(2)
                waiting_for("dark_logo.PNG", confidence=0.8)

                for i in range(60):
                    time.sleep(10)
                    playbtn = check_exist("playbtn.PNG", confidence=0.8)
                    if playbtn:
                        pyautogui.click(playbtn, duration=1)

                    playbtn = check_exist("play_btn_2.PNG", confidence=0.8)
                    if playbtn:
                        pyautogui.click(playbtn, duration=1)

                buttons = ['share_btn_1.PNG', 'share_btn.PNG']
                share_x, share_y, idx = deciscion(buttons)
                pyautogui.click(share_x, share_y)
                click_to("options.PNG", confidence=0.8, interval=2, waiting_time=10)
                click_to("share_to_group.PNG", confidence=0.8, interval=2)

                pyautogui.moveTo(relative_position(1027, 549), duration=1)
                share_box_x, share_box_y = relative_position(x=707, y=378)
                relative_w, relative_h = relative_position(x=1525, y=894)
                if random.choice([0, 1]) == 0:
                    pyautogui.scroll(-200)

                groups = pyautogui.locateAllOnScreen(f"btn/public_group.PNG", confidence=0.8,
                                                     region=(share_box_x, share_box_y, relative_w, relative_h))
                groups = list(groups)
                group = random.choice(groups)
                pyautogui.click(group, duration=2)

                post_btn = waiting_for("post.PNG", confidence=0.8, waiting_time=20)
                if post_btn:
                    title = get_title()
                    paste_text(title)
                    click_to("post.PNG", confidence=0.8)
                    click_to("post_success.PNG", confidence=0.8)