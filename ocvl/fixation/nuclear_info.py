from PySide6 import QtWidgets
from PySide6.QtWidgets import QLabel, QFormLayout, QWidget, QGroupBox


class NuclearInfo(QtWidgets.QWidget):
    def __init__(self, eye, sub_id, save_loc, device):
        """
        sets up information labels based off of user input from initial dialog
        :param eye:
        :param sub_id:
        :param save_loc:
        :param device:
        """
        super().__init__()

        layout = QFormLayout(self)

        self.eye_disp = QtWidgets.QLabel(eye)
        self.id_disp = QtWidgets.QLabel(sub_id)
        self.save_disp = QtWidgets.QLabel(save_loc)
        self.device_disp = QtWidgets.QLabel(device)
        self.FOV_disp = QtWidgets.QLabel("2.0 x 2.0")  # will need to populate with actual fov

        layout.addRow("Eye:", self.eye_disp)
        layout.addRow("Subject ID:", self.id_disp)
        layout.addRow("Device:", self.device_disp)
        layout.addRow(QLabel(""))
        layout.addRow("FOV:", self.FOV_disp)
        layout.addRow(QLabel(""))
        layout.addRow(QLabel("Document Save Location:"))
        layout.addRow(self.save_disp)





