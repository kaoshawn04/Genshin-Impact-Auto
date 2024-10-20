import pyuac
import pyautogui

from time import sleep


def scroll(clicks):
    for _ in range(5):
        pyautogui.scroll(int(clicks / 5))
        sleep(1 / 5)

def take_picture_and_save():
    pyautogui.press("z")
    sleep(0.5)
    pyautogui.dragTo(x=1279.5, y=900, duration=0.5, button="left")
    scroll(-10)
    sleep(0.5)
    pyautogui.press("enter")
    sleep(0.5)
    
    pyautogui.moveTo(x=1275, y=1115)
    sleep(0.5)
    pyautogui.click()
    sleep(0.5)
    
    pyautogui.press("esc")
    sleep(0.5)
    pyautogui.press("esc")
    sleep(0.5)
    
    sleep(5.5)
        

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    
    
    sleep(5)

    for _ in range(24 * 6):
        take_picture_and_save()