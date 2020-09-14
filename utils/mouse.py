"""
操作鼠标键盘
"""
import pyautogui

pyautogui.PAUSE = 1.5  # 每个函数执行后停顿1.5秒
pyautogui.FAILSAFE = True  # 鼠标移到左上角会触发FailSafeException，因此快速移动鼠标到左上角也可以停止


def t1():
    screenWidth, screenHeight = pyautogui.size()  # 屏幕尺寸
    mouseX, mouseY = pyautogui.position()  # 返回当前鼠标位置，注意坐标系统中左上方是(0, 0)
    print(mouseX, mouseY)
    """
    坐标：1350, 1050；下一题坐标
    坐标：150, 560；160, 730；160, 770；显示答案
    坐标：1780, 1050； 截图保存
    坐标：745, 555；保存到文件夹
    """

    while True:
        # 1. 显示答案
        pyautogui.moveTo(160, 560, duration=1)
        pyautogui.click()

        # 2. 按下截图按钮
        pyautogui.hotkey('alt', 'a')
        pyautogui.click()

        # 3. 截图保存
        pyautogui.moveTo(1780, 1050, duration=1)
        pyautogui.click()

        # 4. 保存到文件夹
        pyautogui.moveTo(745, 555, duration=1)
        pyautogui.click()

        # 5. 下一题
        pyautogui.moveTo(1350, 1050, duration=1)
        pyautogui.click()


def t2():
    pyautogui.scroll(2000)
    pass


if __name__ == '__main__':
    pyautogui.moveTo(1480, 800, duration=1)
    pyautogui.click()
    pyautogui.doubleClick()

    pyautogui.typewrite('2222')
    pyautogui.moveTo(1570, 800, duration=1)
    pyautogui.click()
