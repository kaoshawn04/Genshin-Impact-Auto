from library.windows.api import Windows_api


window_names = ["Genshin Impact", "原神"]

for winodw_name in window_names:
    hwnd = Windows_api.find_window(winodw_name)
    
    if hwnd is not None:
        break
    

