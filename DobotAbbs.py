import sys
sys.path.insert(1,'./DLL')
import DobotDllType as DMag


"""-------The DoBot Control Class-------
Variables:
suction = Suction is currently on/off
picking: shows if the dobot is currently picking or dropping an item
api = variable for accessing the dobot .dll functions
home% = home position for %
                                  """

CON_STR = {
    DMag.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    DMag.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    DMag.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
}

#Main control class for the DoBot Magician.
class DBA:
    def __init__(self, homeX, homeY, homeZ):
        self.suction = False
        self.picking = False
        self.api = DMag.load()
        self.homeX = homeX
        self.homeY = homeY
        self.homeZ = homeZ
        self.connected = False
        self.dobotConnect()

    def __del__(self):
        self.dobotDisconnect()

    #Attempts to connect to the dobot
    def dobotConnect(self):
        if(self.connected):
            print("You're already connected")
        else:
            state = DMag.ConnectDobot(self.api, "", 115200)[0]
            if(state == DMag.DobotConnect.DobotConnect_NoError):
                print("Connect status:",CON_STR[state])
                DMag.SetQueuedCmdClear(self.api)

                DMag.SetHOMEParams(self.api, self.homeX, self.homeY, self.homeZ, 0, isQueued = 1)
                DMag.SetPTPJointParams(self.api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
                DMag.SetPTPCommonParams(self.api, 100, 100, isQueued = 1)

                DMag.SetHOMECmd(self.api, temp = 0, isQueued = 1)
                self.connected = True
                return self.connected
            else:
                print("Unable to connect")
                print("Connect status:",CON_STR[state])
                return self.connected

    #Returns to home location and then disconnects
    def dobotDisconnect(self):
        self.moveHome()
        DMag.DisconnectDobot(self.api)

    #Delays commands
    def commandDelay(self, lastIndex):
        DMag.SetQueuedCmdStartExec(self.api)
        while lastIndex > DMag.GetQueuedCmdCurrentIndex(self.api)[0]:
            DMag.dSleep(200)
        DMag.SetQueuedCmdStopExec(self.api)

    #Toggles suction peripheral on/off
    def toggleSuction(self):
        lastIndex = 0
        if(self.suction):
            lastIndex = DMag.SetEndEffectorSuctionCup( self.api, True, False, isQueued = 0)[0]
            self.suction = False
        else:
            lastIndex = DMag.SetEndEffectorSuctionCup(self.api, True, True, isQueued = 0)[0]
            self.suction = True
        self.commandDelay(lastIndex)

    #Moves arm to X/Y/Z Location
    def moveArmXY(self,x,y):
        lastIndex = DMag.SetPTPCmd(self.api, DMag.PTPMode.PTPMOVLXYZMode, x, y, self.homeZ, 0)[0]
        self.commandDelay(lastIndex)

    #Returns to home location
    def moveHome(self):
        lastIndex = DMag.SetPTPCmd(self.api, DMag.PTPMode.PTPMOVLXYZMode, self.homeX, self.homeY, self.homeZ, 0)[0]
        self.commandDelay(lastIndex)

    #Toggles between hover and item level
    def pickToggle(self, itemHeight):
        lastIndex = 0
        positions = DMag.GetPose(self.api)
        if(self.picking):
            lastIndex = DMag.SetPTPCmd(self.api, DMag.PTPMode.PTPMOVLXYZMode, positions[0], positions[1], self.homeZ, 0)[0]
            self.picking = False
        else:
            lastIndex = DMag.SetPTPCmd(self.api, DMag.PTPMode.PTPMOVLXYZMode, positions[0], positions[1], itemHeight, 0)[0]
            self.picking = True
        self.commandDelay(lastIndex)