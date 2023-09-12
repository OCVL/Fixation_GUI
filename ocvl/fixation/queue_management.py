from PySide6.QtGui import Qt


class QueueMgmt:

    def __init__(self, var, parent=None):
        self.var = var

        self.FOV = "1"
        self.VIDNUM = "0"
        self.queue_mgmt()

    def queue_mgmt(self):

        while True:
            if not self.var.recvQ.empty():
                data = self.var.recvQ.get()
                parsed = data.split(";")
                # extract data from message
                if parsed[0] == self.FOV:
                    self.var.current_fov = parsed[1] + ' x ' + parsed[2][0:-1]
                    self.var.control_ref.target.updateFOVText()
                    self.tmp = parsed[1] + ' x ' + parsed[2][0:-1]

                elif parsed[0] == self.VIDNUM:
                    self.var.vid_num = parsed[1][0:-1]
                    self.var.notes_ref.target.addRow()
                    if not self.var.control_ref.target.fov_list.findItems(self.tmp, Qt.MatchFixedString | Qt.MatchCaseSensitive):  # edit: corrected
                        self.var.control_ref.target.fov_list.addItem(self.tmp)
                else:
                    print("Queue Management Shit hit the fan")

