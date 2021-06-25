import pyautogui
import pyperclip
import os
import time
from utils import click_to, waiting_for, deciscion


if os.path.isfile("pass.txt"):
    os.remove("pass.txt")
if os.path.isfile("failed.txt"):
    os.remove("failed.txt")
# pyautogui.moveTo(1756, 200, duration=3)
failed = 0
passed = 0
with open("New-236.txt", encoding='utf-8') as file:
    for line in file.readlines():
        line = line.strip()
        if line != "":
            print(f"cookies: {line}")
            print(f"passed : {passed}")
            print(f"failed : {failed}")
            click_to("app.png")
            import_x, import_y = waiting_for("import.png")
            print("click import btn")
            pyautogui.click(import_x-200, import_y+160)
            pyperclip.copy(line)
            pyautogui.hotkey('ctrlleft', 'v')
            click_to('import.png')
            count = 0
            while True:
                click_to("check_page.PNG")

                # time.sleep(1.5)
                if deciscion(["pass_3.PNG", "pass_6.PNG"]) or count > 5:
                    print("passed")
                    with open("pass.txt", "a", encoding='utf-8') as myfile:
                        myfile.write(line + '\n')
                        passed += 1
                        break
                        
                if deciscion(["failed1.PNG", "failed5.PNG", 'lock.PNG']):
                    print("failed")
                    with open("failed.txt", "a", encoding='utf-8') as myfile:
                        myfile.write(line + '\n')
                        failed += 1
                        break

                count += 1
                print(f"retry {count}")

        # pyautogui.keyDown("esc")
