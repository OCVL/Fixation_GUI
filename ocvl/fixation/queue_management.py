from ocvl.fixation.nuclear_controls import Tabs

class QueueMgmt():

    def __init__(self, var, parent=None):
        self.var = var

        self.FOV = "(0"
        self.VIDNUM = "(1"
        self.queue_mgmt()


    def queue_mgmt(self):

        while True:
            if not self.var.recvQ.empty():
                data = self.var.recvQ.get()
                parsed = data.split(",")
                # print(parsed[0])
                # extract data from message
                if parsed[0] == self.FOV:
                    self.var.current_fov = parsed[1] + ' x ' + parsed[2][0:-1]
                    self.var.control_ref.target.updateFOVText()
                    print("FOV")
                    print(data)
                elif parsed[0] == self.VIDNUM:
                    print("VIDNUM")
                    print(data)
                else:
                    print("Shit hit the fan")

