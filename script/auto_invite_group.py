import time
import pyautogui
from utils import logger, click_to, click_many, check_exist, waiting_for
import pytesseract
# pip install paddlepaddle==2.0.0 -i https://mirror.baidu.com/pypi/simple


def inviting():
    while True:
        # waiting_for("send_invite_group.PNG")
        time.sleep(1)
        click_many("check_box.PNG", confidence=0.98)
        pyautogui.moveTo(1035, 751)
        pyautogui.scroll(-700)
        if check_exist("da_chon.PNG"):
            x, y = waiting_for("da_chon.PNG", confidence=.8)
            img = pyautogui.screenshot(region=(x - 50, y - 30, 200, 50))
            # img.show()
            # custom_config = r'--oem 3 --psm 6'
            texts = pytesseract.image_to_string(img)
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
    number_invited = 0
    # click_to("start_invite_group.PNG")
    # inviting()
    # click_to("send_invite_group.PNG")
    if check_exist("da_chon.PNG"):
        x, y = waiting_for("da_chon.PNG", confidence=.8)
        img = pyautogui.screenshot(region=(x - 150, y - 30, 200, 50))
        # img.show()
        # custom_config = r'--oem 3 --psm 6'
        texts = pytesseract.image_to_string(img)
        for text in texts.split(' '):
            try:
                text = text.strip()
                number_invited = int(text)
                print(f"number invited: {number_invited}")
                # if number_invited > 300:
                    # return True
            except:
                pass