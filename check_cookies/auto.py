import pyperclip
import os
from check_cookies.utils import *

# if os.path.isfile("pass.txt"):
#     os.remove("pass.txt")
# if os.path.isfile("failed.txt"):
#     os.remove("failed.txt")

failed = 0
passed = 0
with open("new6-7.txt", encoding='utf-8') as file:
    for line in file.readlines():
        line = line.strip()
        if line != "":
            logger.info(f"cookies: {line}")
            logger.info(f"number passed : {passed}")
            logger.info(f"number failed : {failed}")
            # if not check_exist("import.png"):
            click_to("app.png")
            # click_to("import.png")

            left, top = waiting_for("import.png")
            pyautogui.click(left, top - 50)
            paste_text(line)
            click_to("import.png")
            click_to("check_page.PNG")

            # time.sleep(1.5)
            buttons = ["cookies_alive_1.PNG", "dark_logo.PNG", "cookies_failed.PNG",
                       "cookies_failed_1.PNG", "cookies_failed_2.PNG"]
            result = deciscion(buttons)
            if result:
                x, y, btn_index = result
                if btn_index == 0 or btn_index == 1:
                    with open("pass.txt", "a", encoding='utf-8') as myfile:
                        myfile.write(line + '\n')
                        passed += 1
                        myfile.close()
                        logger.info("cookies passed")
                else:
                    with open("failed.txt", "a", encoding='utf-8') as myfile:
                        myfile.write(line + '\n')
                        failed += 1
                        myfile.close()
                        logger.info("cookies failed")
            else:
                with open("failed.txt", "a", encoding='utf-8') as myfile:
                    myfile.write(line + '\n')
                    failed += 1
                    myfile.close()
                    logger.info("cookies failed")
