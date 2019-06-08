import pyautogui
import time

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True
width, height = pyautogui.size()

def runInSquare():
	time.sleep(3)
	pyautogui.moveTo(round(width * 0.4), round(height * 0.4), duration=0.25)
	pyautogui.click()
	pyautogui.moveTo(round(width * 0.4), round(height * 0.8), duration=0.25)
	pyautogui.click()
	pyautogui.moveTo(round(width * 0.8), round(height * 0.8), duration=0.25)
	pyautogui.click()
	pyautogui.moveTo(round(width * 0.8), round(height * 0.4), duration=0.25)
	pyautogui.click()

runInSquare()
