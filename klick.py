import ctypes
import datetime
import schedule
from pynput.keyboard import Controller
import time
import win32api, win32con



keyboard = Controller()  # Create the controller
#http://www.philipstorr.id.au/pcbook/book3/scancode.htm key code list


SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def antiafk():


    PressKey(0x11)
    time.sleep(0.1)
    ReleaseKey(0x11)
    time.sleep(0.1)
    PressKey(0x1F)
    time.sleep(0.1)
    ReleaseKey(0x1F)
    now = datetime.datetime.now()
    print("moved : "  + now.strftime("%Y-%m-%d %H:%M:%S"))


#schedule.every(10).seconds.do(antiafk)





def clickLeft(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(0.6)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    time.sleep(0.6)

def clickRight(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    time.sleep(0.6)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
    time.sleep(0.6)



#SCROLL 1590, 530
#row1 1635, 380
def main():
    SCROLLX= 1590
    SCROLLY = 530
    startPosY = 380
    startPosX = 1635
    time.sleep(4)
    for x in range (5):
        
        clickRight(startPosX + x *50,startPosY)
        time.sleep(0.3)
        clickRight(SCROLLX,SCROLLY)
        time.sleep(0.3)
        clickLeft(1655,280)
        clickLeft(1625,350)
        PressKey(0x1D)
        time.sleep(0.1)
        ReleaseKey(0x1D)
        PressKey(0x1B)
        time.sleep(0.1)
        ReleaseKey(0x1B)

    

#while True:
    #schedule.run_pending()
    #time.sleep(1)


main()