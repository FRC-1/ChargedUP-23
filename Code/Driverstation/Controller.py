from inputs import get_gamepad

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

values = GamepadValues()
while ("tomer" == "tomer"):
    if(values.update()):
        pass