import os
import random
import time
from datetime import datetime

import clipboard
import pymongo
import uuid
import schedule
import pyautogui
import pytesseract
from auto_share.utils import click_to, click_many, check_exist, paste_text, typeing_text, waiting_for, deciscion, \
    relative_position, get_title, scheduler_table, logger, group_table
pyautogui.PAUSE = 0.2


def show_desktop():
    pyautogui.click(1635, 1065, button="RIGHT")
    click_to("show_desktop.PNG")


def access_video(video_id):
    reload_bar = waiting_for("reload_bar.PNG", waiting_time=15)
    if reload_bar:
        bar_x, bar_y = reload_bar
        bar_y += 0
        pyautogui.click(bar_x + 100, bar_y)
        # pyautogui.hotkey('ctrl', 'a')
        #
        # paste_text('fb.com')
        # pyautogui.hotkey('enter')
        # waiting_for("dark_logo.PNG", waiting_time=10)

        pyautogui.click(bar_x + 100, bar_y)
        pyautogui.hotkey('ctrl', 'a')
        if video_id:
            paste_text(f"fb.com/{video_id}")
        else:
            paste_text(f"fb.com")
        pyautogui.hotkey('enter')


def auto_share():
    current_hour = datetime.now().hour
    # if current_hour % 2 != 0:
    #     return
    shared_via = []
    time.sleep(5)
    logger.debug("start share")
    show_desktop()
    browsers = pyautogui.locateAllOnScreen(f"btn/coccoc.PNG", confidence=0.95)
    for browser in browsers:
        st = time.time()
        scheduler = scheduler_table.find({"shared": False, "share_number": {"$gt": 0}}).sort("create_date", pymongo.ASCENDING)
        scheduler = list(scheduler)
        if len(scheduler) > 0:
            scheduler = scheduler[0]
            share_number = scheduler.get("share_number", 1)
            groups_shared = scheduler.get('groups_shared', [])
            # group_type = scheduler.get("group_type", ["go", "co_khi", "xay_dung"])
            share_number -= 1
            update_data = {"share_number": share_number}
            if share_number == 0:
                update_data['shared'] = True

            video_id = scheduler['video_id']
            logger.debug(f"share video {video_id}")
            pyautogui.click(997, 452)
            if not check_exist("coccoc.PNG"):
                show_desktop()

            pyautogui.click(browser)
            pyautogui.press('f2')
            pyautogui.hotkey('ctrl', 'c')
            via_name = clipboard.paste()
            if via_name in shared_via:
                continue

            shared_via.append(via_name)
            logger.info(f"click to: {browser}, via_name {via_name}")
            pyautogui.press('enter')
            pyautogui.press('enter')
            click_to("signin.PNG", waiting_time=10)

            pyautogui.moveTo(1027, 549)
            if waiting_for("reload_bar.PNG"):
                click_to("fullscreen_btn.PNG", waiting_time=5)

            access_video(None)
            # check dark theme
            buttons = ['light_logo.PNG', 'dark_logo.PNG']
            deciscion_results = deciscion(buttons)
            if deciscion_results:
                btn_x, btn_y, btn_index = deciscion_results
                if btn_index == 0:
                    # change theme
                    click_to("light_dropdown.PNG")
                    click_to("theme_btn.PNG")
                    click_to("confirm_change.PNG")
                    click_to('dark_logo.PNG')

            waiting_for("dark_logo.PNG")
            if not waiting_for("search_title.PNG", waiting_time=15):
                # change language
                reload_bar = waiting_for("reload_bar.PNG", waiting_time=15)
                if reload_bar:
                    bar_x, bar_y = reload_bar
                    bar_y += 0
                    pyautogui.click(bar_x + 100, bar_y)
                    pyautogui.hotkey('ctrl', 'a')
                    paste_text("https://www.facebook.com/settings?tab=language")
                    pyautogui.hotkey('enter')
                    click_to("English.PNG")
                    pyautogui.press('f5')
                    time.sleep(5)
                    waiting_for("dark_logo.PNG")
                    access_video(video_id)
            else:
                access_video(video_id)
            if waiting_for("dark_logo.PNG", waiting_time=20):
                for i in range(60):
                    time.sleep(1)
                    playbtn = check_exist("playbtn.PNG", confidence=0.85)
                    if playbtn:
                        pyautogui.moveTo(playbtn)
                        pyautogui.click(playbtn)
                    playbtn = check_exist("play_btn_2.PNG", confidence=0.85)
                    if playbtn:
                        pyautogui.moveTo(playbtn)
                        pyautogui.click(playbtn)

                # click share buttons
                buttons = ['share_btn_1.PNG', 'share_btn.PNG']
                result = deciscion(buttons, confidence=0.9)
                if result:
                    share_x, share_y, idx = result
                    pyautogui.click(share_x, share_y)
                else:
                    continue

                # click options or share to a group
                buttons = ["share_to_group.PNG", "options.PNG"]
                result = deciscion(buttons, confidence=0.9)
                if result:
                    share_x, share_y, idx = result
                    pyautogui.click(share_x, share_y, interval=1)
                    if idx == 1:
                        click_to("share_to_group.PNG", confidence=0.9)
                else:
                    continue

                with open("groups.txt", encoding='utf-8') as group_file:
                    for line in group_file.readlines():
                        group_name = line.strip()
                        # try:
                        #     os.makedirs("debug", exist_ok=True)
                        #     img.save(f"debug/{group_name}.PNG")
                        # except Exception as ex:
                        #     pass
                        search_for_group = waiting_for("search_for_group.PNG", waiting_time=10)
                        if search_for_group:
                            search_x, search_y = search_for_group
                            pyautogui.click(search_x+100, search_y)
                            pyautogui.hotkey('ctrl', 'a')
                            paste_text(group_name)
                            if waiting_for("public_group.PNG", waiting_time=10) and group_name not in groups_shared:
                                logger.info(f"found group name: {group_name}")
                                groups_shared.append(group_name)
                                scheduler_table.update_one({"_id": scheduler['_id']},
                                                           {"$set": {"groups_shared": groups_shared}})
                                click_to("public_group.PNG")
                                break
                            else:
                                pyautogui.hotkey('ctrl', 'a')
                                pyautogui.press('backspace')

                post_btn = waiting_for("post.PNG", confidence=0.8, waiting_time=20)
                if post_btn:
                    title = scheduler['title'] if 'title' in scheduler else get_title()
                    typeing_text(title)
                    time.sleep(5)
                    click_to("post.PNG", confidence=0.8, duration=1, interval=3, waiting_time=20)
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
                    else:
                        # click_many("close_btn.PNG")
                        click_to("dark_logo.PNG", confidence=0.9)
                        scheduler_table.update_one({"_id": scheduler['_id']}, {"$set": update_data})
                pyautogui.hotkey('ctrl', 'f4')

        et = time.time()
        logger.debug(f"share done time consuming: {round((et - st)/60, 1)}")
        pyautogui.hotkey('windows', 'd')


def watch_videos():
    logger.info("Start watch video")
    current_hour = datetime.now().hour
    # if current_hour % 2 == 0:
    #     return

    time.sleep(2)
    logger.debug("start share")
    pyautogui.click(1024, 1024)
    pyautogui.hotkey('windows', 'd')
    browsers = pyautogui.locateAllOnScreen(f"btn/coccoc.PNG", confidence=0.95)
    for browser in browsers:
        st = time.time()

        pyautogui.click(browser)
        pyautogui.press('f2')
        pyautogui.hotkey('ctrl', 'c')
        via_name = clipboard.paste()
        logger.info(f"click to: {browser}, via_name {via_name}")
        pyautogui.press('enter')
        pyautogui.press('enter')

        if waiting_for("reload_bar.PNG", waiting_time=15):
            click_to("fullscreen_btn.PNG", waiting_time=5)

        click_to("signin.PNG", waiting_time=10)

        pyautogui.moveTo(1027, 549)
        access_video(None)
        # check dark theme
        buttons = ['light_logo.PNG', 'dark_logo.PNG']
        btn_x, btn_y, btn_index = deciscion(buttons)
        if btn_index == 0:
            # change theme
            click_to("light_dropdown.PNG")
            click_to("theme_btn.PNG")
            click_to("confirm_change.PNG")
            access_video(None)

        waiting_for("dark_logo.PNG")
        if not waiting_for("search_title.PNG", waiting_time=15):
            # change language
            reload_bar = waiting_for("reload_bar.PNG", waiting_time=15)
            if reload_bar:
                bar_x, bar_y = reload_bar
                bar_y += 0
                pyautogui.click(bar_x + 100, bar_y)
                pyautogui.hotkey('ctrl', 'a')
                paste_text("https://www.facebook.com/settings?tab=language")
                pyautogui.hotkey('enter')
                click_to("English.PNG")
                pyautogui.press('f5')
                time.sleep(5)
                waiting_for("dark_logo.PNG")
                access_video(None)

        start_btn = waiting_for("start_btn.PNG", waiting_time=20)
        if start_btn:
            pyautogui.click(start_btn)

            for i in range(60):
                time.sleep(1)
                playbtn = check_exist("playbtn.PNG", confidence=0.85)
                if playbtn:
                    pyautogui.moveTo(playbtn)
                    pyautogui.click(playbtn)
                playbtn = check_exist("play_btn_2.PNG", confidence=0.85)
                if playbtn:
                    pyautogui.moveTo(playbtn)
                    pyautogui.click(playbtn)
            if random.choice([0, 1]):
                click_to("like_btn.PNG", confidence=0.9, interval=1, waiting_time=10)
            click_to("dark_logo.PNG", confidence=0.9, waiting_time=10)
        pyautogui.hotkey('ctrl', 'f4')
        pyautogui.hotkey('windows', 'd')


def start_share():
    logger.debug("Start share")
    try:
        auto_share()
        logger.debug("Done share")
    except Exception as ex:
        logger.error(ex)


def start_watch():
    logger.debug("Start watch")
    try:
        watch_videos()
        logger.debug("Done watch")
    except Exception as ex:
        logger.error(ex)


if __name__ == '__main__':
    logger.info("start share video")
    # time.sleep(2)
    # print(pyautogui.position())
    # auto_share()
    # watch_videos()
    schedule.every(5).hours.at(":00").do(start_share)
    # schedule.every(1).hours.at(":00").do(start_watch)
    while True:
        schedule.run_pending()
        time.sleep(1)
