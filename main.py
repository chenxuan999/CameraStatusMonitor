import os
import sys
import time
import shutil
import ctypes
import threading
import winreg
import subprocess
import tkinter as tk
from PIL import Image, ImageTk

# 全局变量
camera_enabled = False
overlay_window = None
overlay_running = True
taskbar_icon = None

# 检查摄像头是否被使用
def check_camera_usage():
    cmd = ['powershell', '-Command', 'Get-Process | Select-String -Pattern "Camera|摄像头|Webcam"']
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        return 'Camera' in output or '摄像头' in output or 'Webcam' in output
    except subprocess.CalledProcessError:
        return False
    except Exception as e:
        print(f"检测摄像头错误: {e}")
        return False

# 更新覆盖窗口
def update_overlay():
    global camera_enabled
    camera_enabled = check_camera_usage()
    if overlay_window is not None:
        if camera_enabled:
            # 显示绿色圆点
            overlay_window.attributes('-alpha', 0.7)
        else:
            # 隐藏绿色圆点
            overlay_window.attributes('-alpha', 0.0)

# 创建覆盖窗口
def create_overlay():
    global overlay_window
    
    overlay_window = tk.Tk()
    overlay_window.overrideredirect(True)
    overlay_window.attributes('-topmost', True)
    overlay_window.attributes('-transparentcolor', 'white')
    
    # 获取屏幕尺寸
    screen_width = overlay_window.winfo_screenwidth()
    screen_height = overlay_window.winfo_screenheight()
    
    # 创建画布
    canvas = tk.Canvas(overlay_window, width=20, height=20, bg='white', highlightthickness=0)
    canvas.pack()
    
    # 绘制绿色圆点
    dot = canvas.create_oval(0, 0, 20, 20, outline='', fill='green')
    
    # 设置位置 - 右下角
    overlay_window.geometry(f'20x20+{screen_width - 25}+{screen_height - 25}')
    
    # 创建任务栏图标
    create_taskbar_icon()
    
    # 监控摄像头状态
    threading.Thread(target=monitor_camera_usage, daemon=True).start()
    
    # 主循环
    while overlay_running:
        overlay_window.update_idletasks()
        overlay_window.update()
        time.sleep(0.1)

# 监控摄像头使用状态
def monitor_camera_usage():
    while overlay_running:
        update_overlay()
        time.sleep(1)

# 创建任务栏图标
def create_taskbar_icon():
    global taskbar_icon
    
    # 创建任务栏图标窗口
    taskbar_icon = tk.Tk()
    taskbar_icon.overrideredirect(True)
    
    # 设置图标
    try:
        icon = Image.open('camera_icon.ico')  # 图标文件路径
        photo = ImageTk.PhotoImage(icon)
        taskbar_icon.tk.call('wm', 'iconphoto', taskbar_icon._w, photo)
    except:
        pass  # 如果图标文件不存在，忽略错误
    
    # 创建右键菜单
    def toggle_overlay():
        global overlay_running
        overlay_running = False
        overlay_window.destroy()
        taskbar_icon.destroy()
        sys.exit()
    
    def show_menu(event):
        menu = tk.Menu(taskbar_icon, tearoff=0)
        menu.add_command(label="关闭绿色圆点并退出", command=toggle_overlay)
        menu.post(event.x_root, event.y_root)
    
    # 绑定右键菜单
    taskbar_icon.bind('<Button-3>', show_menu)
    
    # 隐藏窗口
    taskbar_icon.withdraw()

# 将程序复制到 AppData 目录并设置开机自启动
def setup_autostart():
    appdata_path = os.path.join(os.environ['APPDATA'], "CameraStatusMonitor")
    exe_path = os.path.abspath(sys.argv[0])
    
    if not exe_path.lower().startswith(appdata_path.lower()):
        # 创建目录
        if not os.path.exists(appdata_path):
            os.makedirs(appdata_path)
        
        # 复制程序到 AppData
        shutil.copy2(exe_path, os.path.join(appdata_path, "camera_monitor.exe"))
        
        # 设置开机自启动
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                              r'Software\Microsoft\Windows\CurrentVersion\Run', 
                              0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, "CameraStatusMonitor", 0, winreg.REG_SZ, 
                                 os.path.join(appdata_path, "camera_monitor.exe"))
        except Exception as e:
            print(f"设置开机自启动失败: {e}")
    
    # 程序位置验证
    if not exe_path.lower().startswith(appdata_path.lower()):
        # 重新启动程序在 AppData 中的副本
        os.startfile(os.path.join(appdata_path, "camera_monitor.exe"))
        sys.exit()

if __name__ == "__main__":
    # 设置开机自启动
    setup_autostart()
    
    # 创建覆盖窗口
    create_overlay()
