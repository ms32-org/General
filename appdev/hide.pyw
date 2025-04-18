from win32 import win32gui

taskbar_hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
win32gui.ShowWindow(taskbar_hwnd, 0)