from Utils.Colors import COLOR
import threading
import time
from inputs import get_gamepad, UnpluggedError

class Controller():
    def __init__(self,sch) -> None:
        self.values = GamepadValues()

        self.A_button = Button()
        self.B_button = Button()
        self.X_button = Button()
        self.Y_button = Button()

        self.right_bumper_button = Button()
        self.left_bumper_button = Button()

        self.start_button = Button()
        self.select_button = Button()

        self.dpad_up_button = Button()
        self.dpad_left_button = Button()
        self.dpad_down_button = Button()
        self.dpad_right_button = Button()

        thread = threading.Thread(target=self.update, args=())
        thread.daemon = True
        thread.start()

    def update(self):
        while True:
            try:
                if(self.values.update()):
                    self.A_button.setVal(int(self.values.btn_A))
                    self.B_button.setVal(int(self.values.btn_B))
                    self.X_button.setVal(int(self.values.btn_X))
                    self.Y_button.setVal(int(self.values.btn_Y))

                    self.right_bumper_button.setVal(int(self.values.btn_TR))
                    self.left_bumper_button.setVal(int(self.values.btn_TL))
                    
                    self.start_button.setVal(int(self.values.btn_Start))
                    self.select_button.setVal(int(self.values.btn_Select))
                    
                    self.dpad_up_button.setVal(self.values.dyval)
                    self.dpad_left_button.setVal(-self.values.dxval)
                    self.dpad_down_button.setVal(-self.values.dyval)
                    self.dpad_right_button.setVal(self.values.dxval)
            except UnpluggedError:
                print(COLOR.FAIL,"NO GAMEPAD FOUND",COLOR.RESET)
                exit()
            time.sleep(0.01)

    def getLeftStick(self):
        return (self.values.lxval,self.values.lyval)
    def getRightStick(self):
        return (self.values.rxval,self.values.ryval)
    def getDirectionalPad(self):
        return (self.values.dxval,self.values.dyval)

class Button():
    def __init__(self,press_threshold = 0.5) -> None:
        self.last_value = 0.0
        self.value = 0.0
        self.threshold = press_threshold
        self.can_press = False
        self.can_release = False

    def setVal(self,val):
        self.last_value = self.value
        self.value = val
        if(self.value > self.threshold and self.last_value < self.threshold):
            self.can_press = True
        if(self.value < self.threshold and self.last_value > self.threshold):
            self.can_release = True

    def isPressed(self):
        return self.value > self.threshold
    def isReleased(self):
        return self.value < self.threshold

    def onPress(self): # onPress will only return true once per command loop, if you need more simply use the shouldStart of the command that uses onPress instead.
        if(self.can_press):
            self.can_press = False
            return True
        return False
    def onRelease(self):
        if(self.can_release):
            self.can_release = False
            return True
        return False

class GamepadValues():
    lxval = 0.0
    lyval = 0.0
    rxval = 0.0
    ryval = 0.0

    btn_A = False
    btn_B = False
    btn_X = False
    btn_Y = False

    dxval = 0.0
    dyval = 0.0

    ltval = 0.0
    rtval = 0.0

    btn_TR = False
    btn_TL = False

    btn_Select = False
    btn_Start = False

    def update(self):
        events = get_gamepad()
        for event in events:
            if event.ev_type == "Absolute":
                val = float(event.state / 32767.0)
                if(event.code == 'ABS_X'):
                    self.lxval = val if abs(val) > 0.1 else 0.0
                elif(event.code == 'ABS_Y'):
                    self.lyval = val if abs(val) > 0.1 else 0.0
                elif(event.code == 'ABS_RX'):
                    self.rxval = val if abs(val) > 0.1 else 0.0
                elif(event.code == 'ABS_RY'):
                    self.ryval = val if abs(val) > 0.1 else 0.0
                elif (event.code == 'ABS_HAT0X'):
                    self.dxval = int(event.state)
                elif (event.code == 'ABS_HAT0Y'):
                    self.dyval = -int(event.state)
                elif (event.code == 'ABS_Z'):
                    self.ltval = float(event.state / 255.0)
                elif (event.code == 'ABS_RZ'):
                    self.rtval = float(event.state / 255.0)
                    
            elif event.ev_type == "Key":
                if(event.code == "BTN_SOUTH"):
                    self.btn_A = bool(event.state)
                elif(event.code == "BTN_NORTH"):
                    self.btn_Y = bool(event.state)
                elif(event.code == "BTN_EAST"):
                    self.btn_B = bool(event.state)
                elif(event.code == "BTN_WEST"):
                    self.btn_X = bool(event.state)
                elif(event.code == "BTN_TL"):
                    self.btn_TL = bool(event.state)
                elif(event.code == "BTN_TR"):
                    self.btn_TR = bool(event.state)
                elif(event.code == "BTN_SELECT"):
                    self.btn_Select = bool(event.state)
                elif(event.code == "BTN_START"):
                    self.btn_Start = bool(event.state)
        return len(events) > 0