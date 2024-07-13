import pyautogui
import pygetwindow as gw
import time

pyautogui.FAILSAFE = False
# 需要修改的参数
relative_x1_rate= 0.974609375 #第二个reset坐标x1比例, 往大调是向右，往小调是向左
relative_y1_rate= 0.154453125 #第二个reset坐标y1比例, 往大调是向下，往小调是向上
relative_x2_rate= 0.929609375 #播放按钮坐标x2比例, 往大调是向右，往小调是向左
relative_y2_rate= 0.234453125 #播放按钮坐标y2比例, 往大调是向下，往小调是向上

screen_info = pyautogui.size()
# second_screen_info = pyautogui.size()  # 第二个屏幕的信息
width = screen_info.width
height = screen_info.height
print("分辨率是：")
print("Width:", width)
print("Height:", height)


# 获取当前打开的所有窗口
windows = gw.getAllTitles()
# 打印所有窗口的标题
for windowname in windows:
    if "release.10" in windowname:
        print("窗口标题:", windowname)
        break
        
# 获取窗口句柄
window = gw.getWindowsWithTitle(windowname)[0]  # 替换为你要操作的窗口标题
# 获取窗口位置
window_x, window_y = window.left, window.top

# 点击刷新按钮
relative_x = relative_x1_rate*width  # 例如，要点击窗口内的 x 坐标
relative_y = relative_y1_rate*height  # 例如，要点击窗口内的 y 坐标

# 计算绝对坐标
click_x = window_x + relative_x
click_y = window_y + relative_y

time.sleep(3)

# 移动光标到窗口内的相对位置并点击
pyautogui.moveTo(click_x, click_y, duration=0.1)  # 可选：使用duration控制移动动画
pyautogui.click()


# 点击播放按钮
relative_x2 = relative_x2_rate*width  # 例如，要点击窗口内的 x 坐标
relative_y2 = relative_y2_rate*height  # 例如，要点击窗口内的 y 坐标

# 计算绝对坐标
click_x = window_x + relative_x2
click_y = window_y + relative_y2

time.sleep(3)

# 移动光标到窗口内的相对位置并点击
pyautogui.moveTo(click_x, click_y, duration=0.1)  # 可选：使用duration控制移动动画
pyautogui.click()
