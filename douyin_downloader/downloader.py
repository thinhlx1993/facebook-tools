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


def download_one(table_data, idx, window):
    row = table_data[idx]
    link_season = row[0]
    episode_name = row[1].replace(":", "")
    link_episode = row[2]
    webbrowser.open(link_episode)
    while True:
        if pyautogui.locateOnScreen(f"buttons/logo.PNG"):
            break

    btn = pyautogui.locateOnScreen("buttons/restore_page.PNG")
    if btn:
        pyautogui.click(292, 54)

    os.makedirs("downloaded", exist_ok=True)
    download_status = download(episode_name)
    pyautogui.click(1033, 97)
    pyautogui.hotkey('ctrl', 'w')
    window.write_event_value('-THREAD-', [idx, download_status])  # put a message into queue for GUI

# if __name__ == '__main__':
#     downloader = Downloader()
#     downloader.start_download('https://theofficetv.com/series/2658-the-cosby-show/seasons/1/episodes/1')
