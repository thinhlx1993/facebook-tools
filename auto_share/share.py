import os
import random
import threading
import time
import uuid
from datetime import datetime
import PySimpleGUI as sg
import clipboard
import pymongo
import pyautogui
from utils import click_to, click_many, check_exist, paste_text, typeing_text, waiting_for, deciscion, \
    relative_position, get_title, scheduler_table, logger, group_table
pyautogui.PAUSE = 0.2


def show_desktop():
    pyautogui.click(1635, 1065, button="RIGHT")
    click_to("show_desktop.PNG")


def access_video(video_id):
    waiting_for("dark_logo.PNG", waiting_time=20)
    reload_bar = waiting_for("reload_bar.PNG", waiting_time=20)
    if reload_bar:
        bar_x, bar_y = reload_bar
        bar_y += 0
        pyautogui.click(bar_x + 100, bar_y)
        pyautogui.hotkey('ctrl', 'a')
        if video_id:
            paste_text(f"fb.com/{video_id}")
        else:
            paste_text(f"fb.com")
        pyautogui.hotkey('enter')


def auto_share(table_data, current_index, window, stop):
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
            time.sleep(2)
            click_to("signin.PNG", waiting_time=10)

            pyautogui.moveTo(1027, 549)
            if waiting_for("reload_bar.PNG"):
                click_to("fullscreen_btn.PNG", waiting_time=10)

            access_video(None)
            # check dark theme
            buttons = ['light_logo.PNG', 'dark_logo.PNG']
            btn_x, btn_y, btn_index = deciscion(buttons)
            if btn_index == 0:
                # change theme
                click_to("light_dropdown.PNG")
                click_to("theme_btn.PNG")
                click_to("confirm_change.PNG")
                click_to('dark_logo.PNG')
                pyautogui.press('f5')
                time.sleep(2)

            waiting_for("reload_bar.PNG")
            waiting_for("dark_logo.PNG")
            if not waiting_for("search_title.PNG", waiting_time=10):
                # change language
                reload_bar = waiting_for("reload_bar.PNG")
                if reload_bar:
                    bar_x, bar_y = reload_bar
                    bar_y += 0
                    pyautogui.click(bar_x + 100, bar_y)
                    pyautogui.hotkey('ctrl', 'a')
                    paste_text("https://www.facebook.com/settings?tab=language")
                    pyautogui.hotkey('enter')
                    waiting_for("reload_bar.PNG")
                    click_to("English.PNG")
                    click_to("English.PNG")
                    time.sleep(2)
                    pyautogui.press('f5')
                    time.sleep(2)
                    waiting_for("dark_logo.PNG")

            access_video(video_id)
            waiting_for("dark_logo.PNG")
            waiting_for("reload_bar.PNG")
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
                    if group_name not in groups_shared:
                        # try:
                        #     os.makedirs("debug", exist_ok=True)
                        #     img.save(f"debug/{group_name}.PNG")
                        # except Exception as ex:
                        #     pass
                        search_for_group = waiting_for("search_for_group.PNG")
                        if search_for_group:
                            search_x, search_y = search_for_group
                            pyautogui.click(search_x+100, search_y)
                            # pyautogui.hotkey('ctrl', 'a')
                            paste_text(group_name)
                            if waiting_for("public_group.PNG", waiting_time=10):
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
        waiting_for("reload_bar.PNG")
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
        waiting_for("reload_bar.PNG")
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


def start_share(table_data, current_index, window, stop):
    logger.debug("Start share")
    try:
        auto_share(table_data, current_index, window, stop)
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


def mapping_table(item):
    return [item.get('video_id', ''), len(item.get('groups_shared', [])), item.get('shared', False)]


if __name__ == '__main__':
    sg.theme('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    headings = ['video_id', 'share group', 'share done']  # the text of the headings
    table_default = scheduler_table.find({"shared": False}, {"video_id": 1, "groups_shared": 1, "shared": 1})
    table_default = list(map(mapping_table, list(table_default)))
    layout = [[sg.Text('Video ID'), sg.InputText("", key="video_id"), sg.Button('Add')],
              [sg.Text('SEO Text'), sg.InputText("", key="text_seo")],
               [sg.Table(values=table_default,
                        headings=headings,
                        display_row_numbers=True,
                        justification='right',
                        auto_size_columns=False,
                        col_widths=[20, 20, 15],
                        vertical_scroll_only=False,
                        num_rows=24, key='table')],
              [sg.Button('Start'),
               sg.Button('Remove'),
               sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Auto Share', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        print(f'{event} You entered {values}')
        print('event', event)
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            browserExe = "chrome.exe"
            os.system("taskkill /f /im " + browserExe)
            break
        elif event == 'Start':
            window.Element('Start').Update(text="Sharing")
            stop_threads = False
            current_index = 0
            if len(values['table']) > 0:
                current_index = values['table'][0]
            table_data = window.Element('table').Get()
            thread = threading.Thread(target=start_share,
                                      args=(table_data, current_index, window, lambda: stop_threads,),
                                      daemon=True)
            thread.start()
        elif event == 'Remove':
            removed = values['table']
            table_data = window.Element('table').Get()
            for item in reversed(removed):
                print()
                video_id = table_data[item][0]
                scheduler_table.update_one({"video_id": video_id}, {"$set": {'shared': True}})
                table_data.pop(item)
            window.Element('table').Update(values=table_data)
        elif event == 'Add':
            video_id = values['video_id']
            text_seo = values['text_seo']
            if video_id != "" and text_seo != "":
                exist_scheduler = scheduler_table.find_one({"video_id": video_id})
                if exist_scheduler:
                    scheduler_table.update_one({"_id": exist_scheduler['_id']},
                                               {"$set": {"shared": False, "share_number": 30, "title": text_seo}})

                new_scheduler = {
                    "_id": str(uuid.uuid4()),
                    "video_id": video_id,
                    "title": text_seo,
                    "scheduler_time": datetime.now().timestamp(),
                    "create_date": datetime.now().timestamp(),
                    "shared": False,
                    "share_number": 30
                }

                result = scheduler_table.insert_one(new_scheduler)
                table_default = scheduler_table.find({"shared": False},
                                                     {"video_id": 1, "groups_shared": 1, "shared": 1})
                table_default = list(map(mapping_table, list(table_default)))
                window.Element('table').Update(values=table_default)
                sg.Popup('Them thanh cong', keep_on_top=True)
            else:
                sg.Popup('Them that bai', keep_on_top=True)
    window.close()
