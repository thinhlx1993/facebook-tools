import os
import time
import pyperclip
import pyautogui
import clipboard
import webbrowser
from utils import click_to, click_many, check_exist, paste_text, typeing_text, waiting_for, deciscion, \
    relative_position, get_title, scheduler_table, logger
pyautogui.FAILSAFE = True


def run(table_data, window):
    os.makedirs("downloaded", exist_ok=True)
    for idx, row in enumerate(table_data):
        link, like, status = row
        if status != 'Downloaded':
            logger.info(f"start download {link}")
            time.sleep(5)
            pyautogui.click(relative_position(300, 54))
            pyautogui.typewrite(link)
            pyautogui.hotkey('enter')
            time.sleep(5)
            waiting_for("logo.PNG")
            retry_time = 0
            while retry_time < 5:
                retry_time += 1
                pyautogui.moveTo(relative_position(1027, 549), duration=1)
                pyautogui.click(relative_position(1027, 549))
                time.sleep(5)
                pyautogui.moveTo(relative_position(800, 649), duration=1)
                download_btn = waiting_for("download_btn.PNG")
                if download_btn:
                    pyautogui.click(download_btn, duration=0.5)
                    buttons = ["filename_box.PNG", "download_btn.PNG"]
                    x, y, btn_index = deciscion(buttons)
                    if btn_index == 1:
                        pyautogui.click(x, y)
                    waiting_box = waiting_for("waiting_box.PNG", waiting_time=10)
                    if waiting_box is not None:
                        waiting_box_x, waiting_box_y = waiting_box
                        pyautogui.click(waiting_box_x, waiting_box_y)
                    filename_box = waiting_for("filename_box.PNG")
                    if filename_box:
                        x, y = filename_box
                        pyautogui.click(x+100, y, duration=0.5)
                        pyautogui.hotkey('ctrl', 'a')
                        time.sleep(0.5)
                        pyautogui.hotkey('ctrl', 'c')
                        video_title = clipboard.paste()
                        video_title = f"{like} Likes-{video_title}"
                        clipboard.copy(video_title)
                        pyautogui.hotkey('ctrl', 'v')
                        pyautogui.hotkey('enter')
                        if waiting_for("yes.PNG", waiting_time=10):
                            click_to("yes.PNG")
                        pyautogui.hotkey('ctrl', 'w')
                        break