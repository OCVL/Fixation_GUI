import PySide6
import numpy as np
from PySide6.QtGui import Qt


class QueueMgmt:

    def __init__(self, var, parent=None):
        self.var = var

        self.FOV = "(0"
        self.VIDNUM = "(1"
        self.tmp_fov_list = []
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
                    tmp = parsed[1] + ' x ' + parsed[2][0:-1]
                    self.tmp_fov_list.append(tmp)
                    if not self.var.control_ref.target.fov_list.findItems(tmp, Qt.MatchFixedString | Qt.MatchCaseSensitive):  # edit: corrected
                        self.var.control_ref.target.fov_list.addItem(tmp)

                elif parsed[0] == self.VIDNUM:
                    self.var.vid_num = parsed[1][0:-1]
                    self.var.notes_ref.target.addRow()
                    print("VIDNUM")
                    print(data)
                else:
                    print("Shit hit the fan")

