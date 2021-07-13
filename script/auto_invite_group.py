import sys
import time
import pyautogui
from utils import logger, click_to, click_many, check_exist, waiting_for
import pytesseract
# pip install paddlepaddle==2.0.0 -i https://mirror.baidu.com/pypi/simple
import keyboard  # using module keyboard


def inviting():
    while True:
        # waiting_for("send_invite_group.PNG")
        time.sleep(1)
        click_many("check_box.PNG", confidence=0.98)
        pyautogui.moveTo(1035, 751)
        pyautogui.scroll(-700)
        da_chon_btn = check_exist("da_chon.PNG", confidence=.7)
        if da_chon_btn:
            x, y, w, h = da_chon_btn
            img = pyautogui.screenshot(region=(x - 150, y, 350, 20))
            # img.show()
            # custom_config = r'--oem 3 --psm 6'
            texts = pytesseract.image_to_string(img)
            if texts:
                for text in texts.split(' '):
                    try:
                        text = text.strip()
                        number_invited = int(text)
                        print(f"number invited: {number_invited}")
                        if number_invited > 300:
                            return True
                    except:
                        pass


if __name__ == '__main__':
    # number_invited = 0s
    click_to("start_invite_group.PNG")
    inviting()
    click_to("send_invite_group.PNG")
    # da_chon_btn = check_exist("da_chon.PNG", confidence=.7)
    # if da_chon_btn:
    #     x, y,w,h = da_chon_btn
    #     img = pyautogui.screenshot(region=(x - 150, y, 350, 20))
    #     img.show()
    #     # custom_config = r'--oem 3 --psm 6'
    #     texts = pytesseract.image_to_string(img)
    #     print(texts)
