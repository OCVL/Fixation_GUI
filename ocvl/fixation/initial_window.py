import sys
from tkinter import filedialog
import os

import PySide6
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit, QComboBox, QDialogButtonBox, QFormLayout, \
    QHBoxLayout, QRadioButton, QVBoxLayout, QCheckBox
from PySide6.QtGui import *


class InitialDialog(QDialog):
    """
    Class for the initial dialog box for user inputs
    """
    def __init__(self, var):
        super().__init__()
        self.var = var
        self.loc_label = QLabel("")
        self.save_location_butt = QPushButton("Save Location")
        self.sub_id_tbox = QLineEdit()
        self.device_menu = QComboBox()
        self.buttonBox = None
        self.setWindowTitle("Setup")
        self.var.config_name = os.getcwd() + "\\test_settings.ini"
        # print(self.var.config_name)
        self.setup()

    def setup(self):
        """
        Set up layouts for the dialog box
        :return:
        """
        # Button and connection code to exit pop up when done
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.okay)
        self.buttonBox.rejected.connect(self.cancel)

        # Sets up the layout for the pop-up window
        layout1 = QFormLayout()
        eye_butt_layout = QHBoxLayout()
        save_loc_butt_layout = QHBoxLayout()

        # Eye Radio button generation and slot/signal linking
        left_eye = QRadioButton("OS")
        right_eye = QRadioButton("OD")
        left_eye.toggled.connect(self.eye_slot)
        right_eye.toggled.connect(self.eye_slot)

        # Linking the field where the sub id is listed to be saved for later use
        self.sub_id_tbox.textChanged.connect(self.onTextEnter)

        # Linking the button used to get the save direction and the variable to store this for later use
        self.save_location_butt.clicked.connect(self.on_save_click)

        # Generating and linking the drop-down menu to the signal/slot to save device selected
        # self.device_menu.addItem("Select Device")
        # for x in self.device_list:
        #     self.device_menu.addItem(x)
        #
        # self.device_menu.currentTextChanged.connect(self.on_combobox_changed)

        # Adding the sub widgets to their boxes for display purposes
        save_loc_butt_layout.addWidget(self.save_location_butt)
        eye_butt_layout.addWidget(left_eye)
        eye_butt_layout.addWidget(right_eye)

        # Load protocol button
        protocol_layout = QVBoxLayout()
        load_p_button = QPushButton()
        load_p_button.setText("Load Protocol")  # Need an advance button
        load_p_label = QLabel()

        # Add the slot to the button and add the button and the layout to the group layout
        load_p_button.clicked.connect(self.onPressLoadP)
        protocol_layout.addWidget(load_p_button)  # Should mark locations with size of FOV on display screen
        protocol_layout.addWidget(load_p_label)

        # Add a stimulus Imaging check box
        stim_imaging = QCheckBox("Yes")
        stim_imaging.stateChanged.connect(self.checkBoxResponse)

        # Adding all components to the main layout of the pop-up window
        layout1.addRow("Select Eye:", eye_butt_layout)
        layout1.addRow("Subject ID:", self.sub_id_tbox)
        layout1.addRow("Select Save Location", save_loc_butt_layout)
        layout1.addRow(self.loc_label)
        layout1.addRow("Protocol:", protocol_layout)
        layout1.addRow("Stimulus Imaging:", stim_imaging)

        layout1.addWidget(self.buttonBox)

        # get device from the config file
        self.var.device = self.var.config.get("ALL", "device")

        self.setLayout(layout1)

    def eye_slot(self):
        """
        Slot for the eye selection
        :return:
        """
        button = self.sender()
        if button.isChecked():
            print("Pressed the button called: " + button.text())
            self.var.eye = button.text()

    def onTextEnter(self):
        """
        Slot for the subject ID
        :return:
        """
        self.var.sub_id = self.sub_id_tbox.text()

    def onPressLoadP(self):
        button = self.sender()
        protocol_path = filedialog.askopenfilenames(title='Select the protocol to load', filetypes=[
            ("protocol", ".csv")])
        print(protocol_path)
        button.setText(str(protocol_path))

    def checkBoxResponse(self):
        """
        Slot for if the fixation target is displayed to the subject
        :return:
        """
        button = self.sender()
        txt = button.text()
        match txt:
            case "Target Animation":
                print(button.checkState())
            case "Target Visible":
                if button.checkState() == PySide6.QtCore.Qt.CheckState.Unchecked:
                    self.var.stimulus_imaging = False
                    print(self.var.stimulus_imaging)
                else:
                    self.var.stimulus_imaging = True
            case "Grid Visible":
                print(button.checkState())
            case _:
                print("Something went wrong!")
        print(txt)

    def on_save_click(self):
        """
        Slot for the save location button
        :return:
        """
        self.var.save_loc = filedialog.askdirectory(title='Select the save location for generated files.')
        self.loc_label.setText(self.var.save_loc)

    # def on_combobox_changed(self):
    #     """
    #     Slot for the device selection drop down
    #     :return:
    #     """
    #     self.var.device = self.device_menu.currentText()

    def okay(self):
        """
        Slot for the okay button. Checks that everything is filled out before continue
        :return:
        """
        # if (self.eye_selected is not None) and (self.subject_id is not None) and (self.subject_id != "") and (self.save_location_dir is not None) and (self.device_selected is not None):
        self.accept()

    def cancel(self):
        """
        Slot for cancel button. Quits application.
        :return:
        """
        sys.exit()

