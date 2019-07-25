# WORKS IN BDO
# RUN AS ADMIN
# !!!!!!!!!!!
import win32api, win32con
import ctypes
import sys, os
import time
import random
import pyautogui
from multiprocessing import Process, Queue

#configure later to make compatible wity different screen sizes,
# by changing functions to sendinput
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

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
6
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# API6
#https://gist.github.com/tracend/912308
class SCANCODE(object):
    ESCAPE        = 0x01
    KB1           = 0x02
    KB2           = 0x03
    KB3           = 0x04
    KB4           = 0x05
    KB5           = 0x06
    KB6           = 0x07
    KB7           = 0x08
    KB8           = 0x09
    KB9           = 0x0A
    KB0           = 0x0B
    MINUS         = 0x0C    #/* - on main keyboard */
    EQUALS        = 0x0D
    BACK          = 0x0E    #/* backspace */
    TAB           = 0x0F
    Q             = 0x10
    W             = 0x11
    E             = 0x12
    R             = 0x13
    T             = 0x14
    Y             = 0x15
    U             = 0x16
    I             = 0x17
    O             = 0x18
    P             = 0x19
    LBRACKET      = 0x1A
    RBRACKET      = 0x1B
    RETURN        = 0x1C    #/* Enter on main keyboard */
    LCONTROL      = 0x1D
    A             = 0x1E
    S             = 0x1F
    D             = 0x20
    F             = 0x21
    G             = 0x22
    H             = 0x23
    J             = 0x24
    K             = 0x25
    L             = 0x26
    SEMICOLON     = 0x27
    APOSTROPHE    = 0x28
    GRAVE         = 0x29    #/* accent grave */
    LSHIFT        = 0x2A
    BACKSLASH     = 0x2B
    Z             = 0x2C
    X             = 0x2D
    C             = 0x2E
    V             = 0x2F
    B             = 0x30
    N             = 0x31
    M             = 0x32
    COMMA         = 0x33
    PERIOD        = 0x34    #/* . on main keyboard */
    SLASH         = 0x35    #/* / on main keyboard */
    RSHIFT        = 0x36
    MULTIPLY      = 0x37    #/* * on numeric keypad */
    LMENU         = 0x38    #/* left Alt */
    SPACE         = 0x39
    CAPITAL       = 0x3A
    F1            = 0x3B
    F2            = 0x3C
    F3            = 0x3D
    F4            = 0x3E
    F5            = 0x3F
    F6            = 0x40
    F7            = 0x41
    F8            = 0x42
    F9            = 0x43
    F10           = 0x44
    NUMLOCK       = 0x45
    SCROLL        = 0x46    #/* Scroll Lock */
    NUMPAD7       = 0x47
    NUMPAD8       = 0x48
    NUMPAD9       = 0x49
    SUBTRACT      = 0x4A    #/* - on numeric keypad */
    NUMPAD4       = 0x4B
    NUMPAD5       = 0x4C
    NUMPAD6       = 0x4D
    ADD           = 0x4E    #/* + on numeric keypad */
    NUMPAD1       = 0x4F
    NUMPAD2       = 0x50
    NUMPAD3       = 0x51
    NUMPAD0       = 0x52
    DECIMAL       = 0x53    #/* . on numeric keypad */
    OEM_102       = 0x56    #/* <> or \| on RT 102-key keyboard (Non-U.S.) */
    F11           = 0x57
    F12           = 0x58
    F13           = 0x64    #/*                     (NEC PC98) */
    F14           = 0x65    #/*                     (NEC PC98) */
    F15           = 0x66    #/*                     (NEC PC98) */
    KANA          = 0x70    #/* (Japanese keyboard)            */
    ABNT_C1       = 0x73    #/* /? on Brazilian keyboard */
    CONVERT       = 0x79    #/* (Japanese keyboard)            */
    NOCONVERT     = 0x7B    #/* (Japanese keyboard)            */
    YEN           = 0x7D    #/* (Japanese keyboard)            */
    ABNT_C2       = 0x7E    #/* Numpad . on Brazilian keyboard */
    NUMPADEQUALS  = 0x8D    #/* = on numeric keypad (NEC PC98) */
    PREVTRACK     = 0x90    #/* Previous Track (CIRCUMFLEX on Japanese keyboard) */
    AT            = 0x91    #/*                     (NEC PC98) */
    COLON         = 0x92    #/*                     (NEC PC98) */
    UNDERLINE     = 0x93    #/*                     (NEC PC98) */
    KANJI         = 0x94    #/* (Japanese keyboard)            */
    STOP          = 0x95    #/*                     (NEC PC98) */
    AX            = 0x96    #/*                     (Japan AX) */
    UNLABELED     = 0x97    #/*                        (J3100) */
    NEXTTRACK     = 0x99    #/* Next Track */
    NUMPADENTER   = 0x9C    #/* Enter on numeric keypad */
    RCONTROL      = 0x9D
    MUTE          = 0xA0    #/* Mute */
    CALCULATOR    = 0xA1    #/* Calculator */
    PLAYPAUSE     = 0xA2    #/* Play / Pause */
    MEDIASTOP     = 0xA4    #/* Media Stop */
    VOLUMEDOWN    = 0xAE    #/* Volume - */
    VOLUMEUP      = 0xB0    #/* Volume + */
    WEBHOME       = 0xB2    #/* Web home */
    NUMPADCOMMA   = 0xB3    #/* , on numeric keypad (NEC PC98) */
    DIVIDE        = 0xB5    #/* / on numeric keypad */
    SYSRQ         = 0xB7
    RMENU         = 0xB8    #/* right Alt */
    PAUSE         = 0xC5    #/* Pause */
    HOME          = 0xC7    #/* Home on arrow keypad */
    UP            = 0xC8    #/* UpArrow on arrow keypad */
    PRIOR         = 0xC9    #/* PgUp on arrow keypad */
    LEFT          = 0xCB    #/* LeftArrow on arrow keypad */
    RIGHT         = 0xCD    #/* RightArrow on arrow keypad */
    END           = 0xCF    #/* End on arrow keypad */
    DOWN          = 0xD0    #/* DownArrow on arrow keypad */
    NEXT          = 0xD1    #/* PgDn on arrow keypad */
    INSERT        = 0xD2    #/* Insert on arrow keypad */
    DELETE        = 0xD3    #/* Delete on arrow keypad */
    LWIN          = 0xDB    #/* Left Windows key */
    RWIN          = 0xDC    #/* Right Windows key */
    APPS          = 0xDD    #/* AppMenu key */
    POWER         = 0xDE    #/* System Power */
    SLEEP         = 0xDF    #/* System Sleep */
    WAKE          = 0xE3    #/* System Wake */
    WEBSEARCH     = 0xE5    #/* Web Search */
    WEBFAVORITES  = 0xE6    #/* Web Favorites */
    WEBREFRESH    = 0xE7    #/* Web Refresh */
    WEBSTOP       = 0xE8    #/* Web Stop */
    WEBFORWARD    = 0xE9    #/* Web Forward */
    WEBBACK       = 0xEA    #/* Web Back */
    MYCOMPUTER    = 0xEB    #/* My Computer */
    MAIL          = 0xEC    #/* Mail */
    MEDIASELECT   = 0xED    #/* Media Select */

def Mousemove():
    ii = Input_I()
    ii.mi = MouseInput(500, 500, 0, 0x8000|0x0001,  )
    x = Input(0, ii)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def PressKey(hScanCode):
    ii = Input_I()
    ii.ki = KeyBdInput(0, hScanCode, 0x0008, 0, None)
    x = Input(1, ii)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hScanCode):
    ii = Input_I()
    ii.ki = KeyBdInput(0, hScanCode, 0x0008 | 0x0002, 0, None)
    x = Input(1, ii)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def PressAndReleaseKey(hScanCode, hold):
    PressKey(hScanCode)
    time.sleep(hold)
    ReleaseKey(hScanCode)

def rand_time():
        x = random.randint(30000,50000)
        x = x/100000
        return x

# Demo
def _mp_worker(command_queue):
    while True:
        scancode, hold, sleepptime = command_queue.get()
        PressAndReleaseKey(scancode, hold)
        print(scancode)
        time.sleep(sleepptime)

def Demo():
    if __name__ == "__main__":
        command_queue = Queue()

        t = Process(target=_mp_worker, args=(command_queue,))
        t.deamon = True
        t.start()

        try:
            while True:
                command_queue.put_nowait([SCANCODE.W, 0.080, 0.1])
                command_queue.put_nowait([SCANCODE.W, 0.080, 0.5])
                command_queue.put_nowait([SCANCODE.A, 0.251, 0.5])
                command_queue.put_nowait([SCANCODE.D, 0.251, 0.5])
                command_queue.put_nowait([SCANCODE.S, 0.551, 0.5])
                time.sleep(5)
        except KeyboardInterrupt:
            print("Goodbye!")

#Mouse click
def click_Right(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    time.sleep(rand_time())
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)

def click_Left(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(rand_time())
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

#mouse Move
def move_mouse(x,y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE|win32con.MOUSEEVENTF_ABSOLUTE, int(round(x/1920*65535.0)), int(round(y/1080*65535.0)), 0, 0)
    print("moved mouse {},{}".format(x,y))
    time.sleep(rand_time())

#Move_warehouse  slot
def click_Warehouse(slot_dx, slot_dy, BUTTON):
    x = random.randint(1090, 1117) + int(round(slot_dx*46.375))
    y = random.randint(316,344) + int(round(slot_dy*46.375))
    move_mouse(x,y)
    click_Right(x, y)
    print("clicked Warehouse at {},{}".format(x, y))
    if BUTTON == "button1":
        time.sleep(rand_time())
        click_Left(x + random.randint(20,129), y + random.randint(16,30))
        print("clicked mount button")
    if BUTTON == "button2":
        time.sleep(rand_time())
        click_Left(x + random.randint(16,129), y + random.randint(66,74))
        print("clicked inventory button")

#move mount clicked
def click_mount_inv(slot_dx, slot_dy, BUTTON):
    x = random.randint(278, 308)  + int(round(slot_dx*46.375))
    y = random.randint(349,377)  + int(round(slot_dy*46.375))
    move_mouse(x,y)
    click_Right(x, y)
    print("clicked mount inventory at {},{}".format(x, y))
    if BUTTON == "button1":
        time.sleep(rand_time())
        click_Left(x + random.randint(20,129), y + random.randint(16,30))
        print("clicked mount button")
    if BUTTON == "button2":
        time.sleep(rand_time())
        click_Left(x + random.randint(16,129), y + random.randint(66,74))
        print("clicked inventory button")

#move inventory click
def click_inventory(slot_dx, slot_dy, BUTTON):
    x = random.randint(1514, 1535) + int(round(slot_dx*46.375))
    y = random.randint(336, 358) + int(round(slot_dy*46.375))
    move_mouse(x,y)
    click_Right(x, y)
    print("clicked own inventory at {},{}".format(x, y))
    if BUTTON == "button1":
        time.sleep(rand_time())
        click_Left(x + random.randint(20,129), y + random.randint(16,30))
        print("clicked mount button")
    if BUTTON == "button2":
        time.sleep(rand_time())
        click_Left(x + random.randint(16,129), y + random.randint(66,74))
        print("clicked inventory button")

#translates numbers into keyboard button input
def KB_weight_input(weight):
    keyboard_input = {0:SCANCODE.KB0, 1:SCANCODE.KB1, 2:SCANCODE.KB2, 3:SCANCODE.KB3,
        4:SCANCODE.KB4, 5:SCANCODE.KB5, 6:SCANCODE.KB6, 7:SCANCODE.KB7, 8:SCANCODE.KB8, 9:SCANCODE.KB9 }

    if weight == "MAX":
        PressAndReleaseKey(SCANCODE.F, rand_time())
        time.sleep(rand_time())
    else:
        for i in range(len(weight)):
            PressAndReleaseKey(keyboard_input[int(weight[i])], rand_time())
            time.sleep(rand_time())

    PressAndReleaseKey(SCANCODE.RETURN, rand_time())  #enter
    print("Entered {} crates".format(weight))

#Mouse pos
def MousePos():
    try:
        while True:
            print(pyautogui.position())
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Good Bye!")

# Run bot
def Run():
    crate_weight = input("Enter the # of crates you can move at a time:")
    max_weight = "9999"
    xslot = int(input("Target crate stack in Warehouse X,Y slot. (Ex: 2nd slot: y=0 x=2)\nEnter X:"))
    yslot = int(input("Enter Y:"))

    print("Starting in:")
    for i in range(6):
        x = 5
        print("{}...".format(x-i))
        time.sleep(1)

    try:
        while True:
            #warehouse 1st slot to inventory transfer
            click_Warehouse(xslot, yslot,"button2")
            time.sleep(rand_time())
            #Keyboard -Crate amount
            KB_weight_input(crate_weight)
            time.sleep(rand_time())

            #mount first slot to inventory transfer
            click_mount_inv(0,0,"button1")
            time.sleep(rand_time())
            #Keyboard -Crate amount
            KB_weight_input("MAX") #max weight = F
            time.sleep(rand_time())

            #inventory to mount transfer
            click_inventory(0,0,"button1")
            time.sleep(rand_time())
            #Keyboard -Crate amount
            KB_weight_input("MAX") #max weight = F
            time.sleep(rand_time())

    except(KeyboardInterrupt):
        print("Good-bye!...")

#State machine
os.system("cls")
print("""
-RUN as ADMIN
-run windowed(fullscreen) at 1080p
-relog to reset your mount inventory window
-Crates will stack to the first slot in your inventory
-Press Ctrl + C in console to terminate bot
================================================================================
""")
state = input("Choose what to run: \n1 - Run Bot\n2 - Mouse Position\n")
options = {1:Run, 2:MousePos}
options[int(state)]()
