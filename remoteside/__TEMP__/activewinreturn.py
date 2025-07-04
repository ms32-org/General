import win32gui
def get_active_window():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd == 0:
        return None, None
    title = win32gui.GetWindowText(hwnd)
    class_name = win32gui.GetClassName(hwnd)
    return title, class_name
# Call this function periodically or triggered by AIM's request
if __name__=="__main__":
    while True:
        print(get_active_window())