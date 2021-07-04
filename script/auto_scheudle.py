import os
import time
import pyautogui
from datetime import datetime
import clipboard

from utils import logger, click_to, click_many, check_exist, waiting_for, paste_text, get_title

os.makedirs('uploaded', exist_ok=True)


if __name__ == '__main__':
    dir_path = r"C:\code\facebook-tools\script\upload"
    while True:
        try:
            # default_date = datetime.strptime(datetime.now(), '%d/%m/%Y %H:%M')
            start_date = pyautogui.prompt(f'Nhập thời gian bắt đầu lên lịch. \nChú ý định dạng kiểu: d/m/YYYY H:M')
            # if start_date == "":
            #     start_date = default_date
            date_time_obj = datetime.strptime(start_date, '%d/%m/%Y %H:%M')
            date_time_obj_ts = date_time_obj.timestamp()
            break
        except Exception as ex:
            pyautogui.alert('Lỗi, Kiểm tra lại định dạng của thời gian bắt đầu')

    for filename in os.listdir(dir_path):
        clipboard.copy(f"{dir_path}\\{filename}")
        click_to("create_new.png")
        click_to("upload_new_video.png")
        time.sleep(2)
        pyautogui.hotkey("ctrl", "v")
        click_to("open.PNG")
        click_to("upload_done.png")
        click_many("close_step.png")

        # paste title
        title = waiting_for("title.png")
        title_x, title_y = title
        pyautogui.click(title_x + 50, title_y)
        filename_without_ext = os.path.splitext(filename)[0] + " #Crafting #Relaxing"
        # fix title
        if '-' in filename_without_ext:
            filename_without_ext = filename_without_ext.split('-')[1]
        paste_text(filename_without_ext)
        description = get_title()
        pyautogui.click(title_x + 50, title_y+70)
        paste_text(description)

        click_to("next.png")
        click_to("later.PNG", waiting_time=2)
        click_to("schedule.PNG")
        schedule_x, schedule_y = waiting_for("auto_schedule.png")

        date_obj = datetime.fromtimestamp(date_time_obj_ts)
        # change date
        pyautogui.click(schedule_x + 30, schedule_y, interval=0.5)
        date = date_obj.strftime("%d/%m/%Y")
        logger.info(f"current date {date}")
        pyautogui.typewrite(date, interval=0.2)

        # change hour
        pyautogui.click(schedule_x + 120, schedule_y, interval=0.5)
        hour = date_obj.strftime("%H")
        logger.info(f"current hour {hour}")
        pyautogui.typewrite(hour, interval=0.2)

        # change time
        pyautogui.click(schedule_x + 130, schedule_y, interval=0.5)
        minute = date_obj.strftime("%M")
        logger.info(f"current minute {minute}")
        pyautogui.typewrite(minute, interval=0.2)
        click_to("finish.png")
        waiting_for("done.png")
        click_to("close_success.PNG", region=(1000, 200, 300, 400))
        date_time_obj_ts += 7200
        move_to_uploaded = f"C:\\code\\facebook-tools\\script\\uploaded\\{filename}"
        if not os.path.isfile(move_to_uploaded):
            os.rename(f"{dir_path}\\{filename}", move_to_uploaded)
