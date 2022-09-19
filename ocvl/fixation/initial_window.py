import configparser
import sys
from tkinter import filedialog

from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit, QComboBox, QDialogButtonBox, QFormLayout, \
    QHBoxLayout, QRadioButton


class InitialDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.subject_id = None
        self.temp_loc_name = QLabel("")
        self.save_location_butt = QPushButton("Save Location")
        self.eye_selected = None
        self.sub_id = QLineEdit()
        self.device_menu = QComboBox()
        self.save_location_dir = None
        self.device_selected = None
        self.buttonBox = None
        self.setWindowTitle("Setup")
        self.config = configparser.ConfigParser()
        self.config_name = filedialog.askopenfilenames(title='Select the configuration file', filetypes=[
            ("configuration file", ".ini")])
        self.config.read(self.config_name)
        self.device_list = self.config.get("ALL", "device_list").split("/")
        self.setup()

    def setup(self):
        # Button and connection code to exit pop up when done
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.okay)
        self.buttonBox.rejected.connect(self.cancel)

        # Sets up the layout for the pop up window
        layout1 = QFormLayout()
        eye_butt_layout = QHBoxLayout()
        save_loc_butt_layout = QHBoxLayout()

        # Eye Radio button generation and slot/signal linking
        left_eye = QRadioButton("OS")
        right_eye = QRadioButton("OD")
        left_eye.toggled.connect(self.eye_slot)
        right_eye.toggled.connect(self.eye_slot)

        # Linking the field where the sub id is listed to be saved for later use
        self.sub_id.textChanged.connect(self.onTextEnter)

        # Linking the button used to get the save direction and the variable to store this for later use
        self.save_location_butt.clicked.connect(self.on_save_click)

        # Generating and linking the drop-down menu to the signal/slot to save device selected
        self.device_menu.addItem("Select Device")
        for x in self.device_list:
            self.device_menu.addItem(x)

        self.device_menu.currentTextChanged.connect(self.on_combobox_changed)

        # Adding the sub widgets to their boxes for display purposes
        save_loc_butt_layout.addWidget(self.save_location_butt)
        eye_butt_layout.addWidget(left_eye)
        eye_butt_layout.addWidget(right_eye)

        # Adding all components to the main layout of the pop up window
        layout1.addRow("Select Eye", eye_butt_layout)
        layout1.addRow("Subject ID:", self.sub_id)
        layout1.addRow("Select Save Location", save_loc_butt_layout)
        layout1.addRow(self.temp_loc_name)
        layout1.addRow("Device", self.device_menu)
        layout1.addWidget(self.buttonBox)

        self.setLayout(layout1)

    def eye_slot(self):
        button = self.sender()
        if button.isChecked():
            print("Pressed the button called: " + button.text())
            self.eye_selected = button.text()

    def onTextEnter(self):
        self.subject_id = self.sub_id.text()

    def on_save_click(self):
        self.save_location_dir = filedialog.askdirectory(title='Select the save location for generated files.')
        self.temp_loc_name.setText(self.save_location_dir)

    def on_combobox_changed(self):
        self.device_selected = self.device_menu.currentText()

    def okay(self):
        # if (self.eye_selected is not None) and (self.subject_id is not None) and (self.subject_id != "") and (self.save_location_dir is not None) and (self.device_selected is not None):
        self.accept()
    def cancel(self):
        sys.exit()

