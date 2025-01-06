with open("C:/Users/kaosh/OneDrive/桌面/Genshin-Impact-Auto/midi/Never_Gonna_Give_You_Up.mid", "rb") as file:
    while byte := file.read(1):
        print(byte.hex(), end=" ")