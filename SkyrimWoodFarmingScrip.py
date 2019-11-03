import ctypes
import time

############################################
# Skyrim Wood Farming Scrip. Version 1.0
############################################
# Moving the camera along the vertical axis.
# Default moving = 800.
############################################
moving = 800
############################################
# Time of one cutting (in seconds).
# Default timeOfCutting = 33.
############################################
timeOfCutting = 33
############################################

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
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def MouseMoveTo(x, y):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(x, y, 0, 0x0001, 0, ctypes.pointer(extra))

    command = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


if __name__ == '__main__':
    print("Enter the number of attempts:", end=" ")
    quantity = int(input())
    print("Start in 5 seconds.")
    for i in range(6)[::-1]:
        print(i, end=" ")
        time.sleep(1)
    print()
    print("Start!")
    for attempt in range(1, quantity + 1):
        MouseMoveTo(0, moving)
        time.sleep(0.1)
        PressKey(0x12)
        time.sleep(0.1)
        ReleaseKey(0x12)
        for i in range(timeOfCutting + 1)[::-1]:
            print(i, end=" ")
            time.sleep(1)
        print()
        print("Done " + str(attempt) + ".")
        print("Wood: " + str(attempt * 6) + ".")
        print("Gold: " + str(attempt * 30) + ".")
        print("Work time: " + str(attempt * timeOfCutting) + " second.")
