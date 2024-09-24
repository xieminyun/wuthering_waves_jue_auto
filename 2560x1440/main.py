import time
import pyautogui
import keyboard
import cv2
import numpy as np

startHotkey = 'alt+s'  # 启动脚本快捷键
stopHotkey = 'alt+d'  # 终止脚本快捷键
gameResolution1 = (0, 0, 2560, 1440)
gameResolution2 = (320, 180, 1920, 1080)
multiPlayReso = (10, 35, 68, 68)
bossHPReso = (890, 71, 26, 26)
absorbReso = (1790, 725, 60, 35)
enterReso = (1790, 725, 180, 35)
ExitSample = 'ExitSample.png'
bossHPSample = 'BossHPSample.png'
absorbSample = 'AbsorbSample.png'
EnterSample = 'EnterSample.png'
absorbedNum = 0

def picCompare(original_img1, original_img2):
    img1 = cv2.imread(original_img1)
    img2 = cv2.imread(original_img2)
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    mean1, mean2 = np.mean(img1_gray), np.mean(img2_gray)
    var1, var2 = np.var(img1_gray), np.var(img2_gray)
    cov = np.cov(img1_gray.flatten(), img2_gray.flatten())[0, 1]
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2
    ssim = (2 * mean1 * mean2 + c1) * (2 * cov + c2) / ((mean1 ** 2 + mean2 ** 2 + c1) * (var1 + var2 + c2))
    return ssim

def checkBossHP():
    pyautogui.screenshot('BossHP.png', bossHPReso)
    bossHP = 'BossHP.png'
    ssim = picCompare(bossHPSample, bossHP)
    if ssim >= 0.3:
        return True
    else:
        return False

def fight():
    pyautogui.press('e')
    pyautogui.click(button='left', interval=0.2, clicks=10)
    pyautogui.press('2')
    pyautogui.press('q')
    pyautogui.click(button='left', interval=0.2, clicks=10)
    pyautogui.press('3')
    time.sleep(0.5)
    pyautogui.press('e')
    pyautogui.press('1')

def checkEcho():
    pyautogui.screenshot('Absorb.png', absorbReso)
    absorb = 'Absorb.png'
    ssim = picCompare(absorb, absorbSample)
    if ssim >= 0.8:
        return True
    else:
        return False

# 吸收声骸
def echo():
    pyautogui.click(button='middle')
    directions = ['w', 'a', 's', 'd']
    for duration in [1, 1, 2, 2, 3, 3, 4, 4]:
        for direction in directions:
            pyautogui.keyDown(direction)
            time.sleep(duration)
            pyautogui.keyUp(direction)
            if checkEcho():
                pyautogui.press('f', presses=2)
                return True
    return False

# 检查是否退出
def checkExit():
    pyautogui.screenshot('Enter.png', enterReso)
    enter = 'Enter.png'
    ssim = picCompare(EnterSample, enter)
    if ssim >= 0.85:
        return True
    else:
        return False

def run():
    # 按F进入时序之寰
    pyautogui.press('f')
    # 选择推荐等级50 点击单人挑战 点击开启挑战
    pyautogui.moveTo(x=423, y=357)
    pyautogui.click(x=423, y=357, button='left', interval=0.5, clicks=3)
    pyautogui.click(x=2077, y=1296, button='left', interval=0.5, clicks=2)
    pyautogui.click(x=2077, y=1296, button='left', interval=0.5, clicks=2)
    # 检测是否成功载入游戏
    while True:
        pyautogui.screenshot('ExitIcon.png', multiPlayReso)
        exitIcon = 'ExitIcon.png'
        ssim = picCompare(ExitSample, exitIcon)
        if ssim >= 0.8:
            break
        time.sleep(0.5)
    # 开始战斗流程
    pyautogui.keyDown('w')
    time.sleep(3)
    pyautogui.keyUp('w')
    while True:
        if checkBossHP():
            fight()
        else:
            if checkBossHP():
                fight()
            else:
                if checkBossHP():
                    fight()
                else:
                    echo()
                    pyautogui.press('esc')
                    pyautogui.click(x=1718, y=893, button='left', interval=0.5, clicks=2)
                    break
    time.sleep(5)

def mainFunc():
    time.sleep(1)
    dur = 0.8
    pyautogui.PAUSE = dur  # 停顿时间
    pyautogui.FAILSAFE = True  # 终止程序、声明异常
    print("开始运行脚本...")
    while not keyboard.is_pressed(stopHotkey):
        pyautogui.click(button='right')
        time.sleep(1)
        if checkExit():
            run()
    print("脚本已终止。")

keyboard.add_hotkey(startHotkey, mainFunc)  # 启动脚本

try:
    print(f"按下 {startHotkey} 启动脚本，按下 {stopHotkey} 终止脚本。")
    keyboard.wait()
except KeyboardInterrupt:
    print("脚本中断。")