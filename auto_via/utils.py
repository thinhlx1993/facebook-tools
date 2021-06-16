import clipboard
import requests
import logging
import pymongo
import pyautogui
import time
import random
import pyotp
import uuid
import re
from bs4 import BeautifulSoup
from bson import ObjectId
from exchangelib import Credentials, Account


# create logger with 'spam_application'
logger = logging.getLogger('application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('app.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


client = pymongo.MongoClient("mongodb+srv://facebook:auft.baff1vawn*WEC@cluster0.dtlfk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test
phone_table = db['phone']
email_table = db['emails']
cookies_table = db['cookies']
via_share_table = db['via_share']


def random_interval():
    return random.uniform(0.5, 2)


def click_to(btn, confidence=0.8, region=None, waiting_time=1000, interval=None, check_close=True):
    logger.info(f"Click to {btn}")
    start_count = 0
    if check_close:
        click_many("x_btn.PNG", confidence=0.95, region=(0, 100, 1920, 900), log=False)
    while start_count < waiting_time:
        ret = pyautogui.locateOnScreen(f"btn/{btn}", confidence=confidence, region=region)
        start_count += 1
        if ret:
            interval = random_interval() if interval is None else interval
            pyautogui.click(ret, interval=interval)
            break
        if pyautogui.locateOnScreen(f"btn/input_password_to_continue.PNG", confidence=0.7, region=region):
            click_to("passowrd_input_txt.PNG")
            paste_text("Minh1234@")
            click_to("input_password_next.PNG", confidence=0.7)
        time.sleep(0.2)


def click_many(btn, region=None, confidence=0.8, log=True):
    if log:
        logger.info(f"Click many {btn}")
    elements = pyautogui.locateAllOnScreen(f"btn/{btn}", confidence=confidence, region=region)
    number_element = len(list(pyautogui.locateAllOnScreen(f"btn/{btn}", confidence=0.85, region=region)))
    for ret in elements:
        pyautogui.click(ret, interval=random_interval())
    return number_element


def check_exist(btn, region=None, confidence=0.8):
    exist = pyautogui.locateOnScreen(f"btn/{btn}", confidence=confidence, region=region)
    logger.info(f"Check exist {btn} result {exist}")
    return exist


def waiting_for(btn, region=None, confidence=0.8, waiting_time=1000):
    logger.info(f"Waiting for {btn}")
    start_count = 0
    while start_count < waiting_time:
        start_count += 1
        ret = pyautogui.locateCenterOnScreen(f"btn/{btn}", confidence=confidence, region=region)
        if ret:
            x, y = ret
            return x, y

        if pyautogui.locateOnScreen(f"btn/input_password_to_continue.PNG", confidence=0.7, region=region):
            click_to("passowrd_input_txt.PNG")
            paste_text("Minh1234@")
            click_to("input_password_next.PNG", confidence=0.7)
        time.sleep(0.2)
    return None


def deciscion(btns, region=None, confidence=0.8):
    while True:
        for btn_index, btn in enumerate(btns):
            logger.info(f"Waiting for {btn}")
            ret = pyautogui.locateCenterOnScreen(f"btn/{btn}", confidence=confidence, region=region)
            if ret:
                x, y = ret
                return x, y, btn_index


def typeing_text(inp_text):
    pyautogui.typewrite(inp_text, interval=0.2)


def paste_text(inp_text):
    clipboard.copy(inp_text)
    pyautogui.hotkey('ctrl', 'v', interval=0.5)


def get_new_phone():
    network = random.randint(1, 6)
#     network = random.choice([1,3,6])
    api_uri = f"https://otpsim.com/api/phones/request?token=8c4be439c12d0e53fd21bfb25cd07b46&service=7"
    while True:
        res = requests.get(api_uri)
        if res.status_code == 200:
            res_json = res.json()
            logger.info(f"Get new phone {res_json}")
            if res_json['status_code'] == 200:
                res_json['_id'] = str(uuid.uuid4())
                res_json['api_type'] = 'get_new_phone'
                phone_table.insert_one(res_json)
                return res_json['data']['phone_number'], res_json['data']['session']
            time.sleep(2)


def get_exist_phone(phone_number):
    api_uri = f"https://otpsim.com/api/phones/request?token=8c4be439c12d0e53fd21bfb25cd07b46&service=7&number={phone_number}"
    res = requests.get(api_uri)
    if res.status_code == 200:
        res_json = res.json()
        logger.info(f"Get exist phone {res_json}")
        if res_json['status_code'] == 200:
            res_json['_id'] = str(uuid.uuid4())
            res_json['api_type'] = 'get_exist_phone'
            phone_table.insert_one(res_json)
            return res_json['data']['session']
    return "", ""


def get_code(session):
    # code = res['data']['messages']['otp']
    api_uri = f"https://otpsim.com/api/sessions/{session}?token=8c4be439c12d0e53fd21bfb25cd07b46"
    st = time.time()
    while True:
        time.sleep(5)
        try:
            res = requests.get(api_uri)
            if res.status_code == 200:
                res_json = res.json()
                logger.info(f"Get code otp {res_json}")
                if res_json['status_code'] == 200:
#                     res_json['_id'] = str(uuid.uuid4())
#                     res_json['api_type'] = 'get_code'
#                     phone_table.insert_one(res_json)
                    data_json = res_json['data']
                    if data_json['status'] == 0:
                        return data_json['messages'][0]['otp']
                current_time = time.time()
                if current_time - st > 20:
                    # waiting for 2 min
                    cancel_session(session)
                    return None
        except Exception as ex:
            logger.error(f'Call api get token errors: {ex}')


def cancel_session(session):
    api_uri = f"https://otpsim.com/api/sessions/cancel?session={session}&token=8c4be439c12d0e53fd21bfb25cd07b46"
    res = requests.get(api_uri)
    res_json = res.json()
    res_json['_id'] = str(uuid.uuid4())
    res_json['api_type'] = 'cancel_session'
    phone_table.insert_one(res_json)
    logger.info(f"cancel session: {session} json {res_json}")
    return True if res.status_code == 200 else False


def get_out_look(email_outlook, email_password):
    credentials = Credentials(email_outlook, email_password)
    account = Account(email_outlook, credentials=credentials, autodiscover=True)
    while True:
        for item in account.inbox.all().order_by('-datetime_received')[:5]:
            if item.sender.email_address == 'security@facebookmail.com':
                print(item.datetime_received)
                soup = BeautifulSoup(item.body, 'html.parser')
                all_tags = soup.find_all('a')
                href = ""
                for tag in all_tags:
                    # href="https://www.facebook.com/confirmcontact.php?c=60029&z=0&gfid=AQDLZ-4fI-MohTeh-Ls"
                    href = tag.get('href')
                    if 'confirmcontact' in href:
                        print(href)
                        break

                otp_code = re.search("\d{5}", item.body)
                if otp_code:
                    start, end = otp_code.span()
                    otp_code = item.body[start: end]
                return href, otp_code


def get_email():
    # check email is access able
    while True:
        email = email_table.find_one({"used": False, "failed": False})
        if email:
            email_outlook = email['email']
            email_password = email['password']
            exist_via = via_share_table.find_one({"email": email_outlook})
            if not exist_via:
                try:
                    credentials = Credentials(email_outlook, email_password)
                    account = Account(email_outlook, credentials=credentials, autodiscover=True)
                    myquery = { "_id": email['_id'] }
                    newvalues = { "$set": { "used": True } }
                    email_table.update_one(myquery, newvalues)
                    logger.info(f"email is not ready: {email_outlook}")
                    return email_outlook, email_password
                except Exception as ex:
                    myquery = { "_id": email['_id'] }
                    newvalues = { "$set": { "failed": True, "used": True } }
                    email_table.update_one(myquery, newvalues)
                    logger.error(f"email is not accessible: {email_outlook}")


def get_fb_id():
    pyautogui.click(x=1709, y=587)
    pyautogui.hotkey('ctrl', 't')
    click_to("home_page.PNG", confidence=0.9)
    pyautogui.click(x=264, y=50, interval=2)
    pyautogui.hotkey('ctrl', 'c')
    click_to("fb_cookies.PNG")
    click_to("get_fb_uid.PNG")
    pyautogui.hotkey('ctrl', 'v')
    click_to("get_id.PNG")
    waiting_for("facebookid_dialog.PNG")
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.press('esc')
    fb_id = clipboard.paste()
    pyautogui.hotkey('ctrl', 'w')
    return fb_id