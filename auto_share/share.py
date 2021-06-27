import random
import time
import schedule
import pyautogui
from datetime import datetime
from utils import click_to, click_many, check_exist, paste_text, typeing_text, waiting_for, deciscion, \
    relative_position, get_title, scheduler_table, logger


def auto_share():
    print("start share")
    scheduler = scheduler_table.find_one({"shared": False})
    if scheduler:
        scheduler_table.update_one({"_id": scheduler['_id']}, {"$set": {"shared": True}})
        video_id = scheduler['video_id']
        logger.info(f"share video {video_id}")
        # time.sleep(2)
        # pyautogui.hotkey('winleft', 'd')
        # time.sleep(1)
        bar_x, bar_y = relative_position(0, 1000)
        width, height = relative_position(1920, 80)
        print(bar_x, bar_y, width, height)
        browsers = pyautogui.locateAllOnScreen(f"btn/coccoc.PNG", confidence=0.9, region=(bar_x, bar_y, width, height))
        # pyautogui.screenshot("1.png", region=(bar_x, bar_y, width, height))
        for browser in browsers:
            pyautogui.click(browser)
            click_to("dark_logo.PNG", confidence=0.9)
            pyautogui.click(relative_position(300, 54))
            paste_text(f"fb.com/{video_id}")
            pyautogui.hotkey('enter')
            time.sleep(2)
            waiting_for("dark_logo.PNG", confidence=0.9)

            for i in range(20):
                time.sleep(1)
                playbtn = check_exist("playbtn.PNG", confidence=0.85)
                if playbtn:
                    pyautogui.moveTo(playbtn)
                    pyautogui.click(playbtn)
                pyautogui.moveTo(relative_position(1027, 549), duration=1)
                pyautogui.moveTo(relative_position(800, 649), duration=1)
                playbtn = check_exist("play_btn_2.PNG", confidence=0.85)
                if playbtn:
                    pyautogui.moveTo(playbtn)
                    pyautogui.click(playbtn)

            # click share buttons
            buttons = ['share_btn_1.PNG', 'share_btn.PNG']
            share_x, share_y, idx = deciscion(buttons)
            pyautogui.click(share_x, share_y, interval=1)

            # click options or share to a group
            buttons = ["options.PNG", "share_to_group.PNG"]
            share_x, share_y, idx = deciscion(buttons)
            pyautogui.click(share_x, share_y, interval=1)
            if idx == 0:
                click_to("share_to_group.PNG", confidence=0.9, interval=1)

            waiting_for("public_group.PNG", confidence=0.85)
            pyautogui.moveTo(relative_position(1027, 549), duration=1)
            time.sleep(2)
            scroll_time = random.choice([1, 2, 3, 4])
            pyautogui.scroll(-200*scroll_time)

            while True:
                try:
                    groups = pyautogui.locateAllOnScreen(f"btn/public_group.PNG", confidence=0.7)
                    groups = list(groups)
                    group = random.choice(groups)
                    pyautogui.click(group, duration=0.5)
                    break
                except Exception as ex:
                    pass

            post_btn = waiting_for("post.PNG", confidence=0.8, waiting_time=20)
            if post_btn:
                title = get_title()
                paste_text(title)
                time.sleep(5)
                click_to("post.PNG", confidence=0.8, duration=1, interval=3)
                click_to("post_success.PNG", confidence=0.8, waiting_time=20)
                spam = waiting_for("spam.PNG", confidence=0.9, waiting_time=10)
                if spam:
                    pyautogui.hotkey('ctrl', 'f4')
                    time.sleep(1)
                    pyautogui.press('enter')
                    time.sleep(1)
                    pyautogui.hotkey('ctrl', 'f4')
                    logger.info("limited")
                # click_to("dark_logo.PNG", confidence=0.9)


if __name__ == '__main__':
    # auto_share()
    schedule.every(2).hours.at(":00").do(auto_share)
    while True:
        schedule.run_pending()
        time.sleep(1)
