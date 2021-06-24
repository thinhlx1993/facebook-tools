import pyautogui
import pyperclip
import os
import time


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
            while True:
                app_btn = pyautogui.locateOnScreen('btn/app.png')
                if app_btn:
                    print("click app btn")
                    pyautogui.click(app_btn)  # Find where button.png appears on the screen and click it.
                    left, top, width, height = app_btn
                    break
                if pyautogui.locateOnScreen('btn/import.png'):
                    print("found import btn")
                    break
                
            while True:
                import_btn = pyautogui.locateOnScreen('btn/import.png')
                if import_btn:
                    print("click import btn")
                    pyperclip.copy(line)
                    pyautogui.click(left-200, top+160)
                    pyautogui.hotkey('ctrlleft', 'v')
                    pyautogui.click(import_btn) # Find where button.png appears on the screen and click it.
                    break
                    
            count = 0
            while True:
                check_page = pyautogui.locateOnScreen("btn/check_page.PNG")
                if check_page:
                    print("check page")
                    pyautogui.click(check_page)
                    time.sleep(0.5)
                    
                # time.sleep(1.5)
                if pyautogui.locateOnScreen("btn/pass_3.PNG") or \
                  pyautogui.locateOnScreen("btn/pass_6.PNG") or \
                  count > 2:
                    print("passed")
                    with open("pass.txt", "a", encoding='utf-8') as myfile:
                        myfile.write(line + '\n')
                        passed += 1
                        break
                        
                if pyautogui.locateOnScreen("btn/failed1.PNG") or \
                    pyautogui.locateOnScreen("btn/failed5.PNG") or \
                    pyautogui.locateOnScreen("btn/lock.PNG"):
                    print("failed")
                    with open("failed.txt", "a", encoding='utf-8') as myfile:
                        myfile.write(line + '\n')
                        failed += 1
                        break
                    break

                count += 1
                print(f"retry {count}")

        # pyautogui.keyDown("esc")
