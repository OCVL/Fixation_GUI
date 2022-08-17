from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtCore
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QTabWidget, QWidget, QFormLayout, QLineEdit, \
    QHBoxLayout, QRadioButton, QSlider, QAbstractSlider, QPushButton, QColorDialog, QVBoxLayout

print(PySide6.__version__)  # Prints the pyside6 version
print(PySide6.QtCore.__version__)  # Prints Qt version used to compile Pyside6


class Tabs(QTabWidget):
    def __init__(self, parent=None):
        super(Tabs, self).__init__(parent)

        # Generate the Tabs for the window to hold the settings
        self.color_label = None
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()

        # Generate class variables used in slots and signals
        self.label_size = None
        self.test_label = None
        self.size_bar = None
        self.image_cal_button = None
        self.load_bg_image_button = None

        # Set the position of the tabs to be on the right
        self.setTabPosition(QTabWidget.East)

        # Add the tabs generated to the parent window
        self.addTab(self.tab1, "Stimulus Control")
        self.addTab(self.tab2, "Fixation Target Control")
        self.addTab(self.tab3, "Image Calibration Control")
        self.addTab(self.tab4, "Protocol Control")
        self.addTab(self.tab5, "Help")

        # Make a UI function for each of the tabs
        self.tab1ui()
        self.tab2ui()
        self.tab3ui()
        self.tab4ui()
        self.tab5ui()

        # Set the Title of the Window
        self.setWindowTitle("Control Settings")

    # Function for the UI of Tab 1 - Stimulus control
    def tab1ui(self):
        layout1 = QFormLayout()
        layout1.addRow("Port Number:", QLineEdit())

        # Create the radio Buttons for the different stimulus options
        stim_opts = QHBoxLayout()
        stim_opts.addWidget(QRadioButton("Animal"))
        stim_opts.addWidget(QRadioButton("Human"))

        layout1.addRow("Stimulus Options: ", stim_opts)

        self.setTabText(0, "Stimulus Control")
        self.tab1.setLayout(layout1)

    # Function for the UI of Tab 2 - Fixation Target Control
    def tab2ui(self):
        layout2 = QFormLayout()

        # Widget for the shape objects for the fixation target
        fix_shape = QHBoxLayout()

        # Color wheel for selecting the color of the target
        self.color_layout = QHBoxLayout()
        color_button = QPushButton("Select Color")
        self.color_layout.addWidget(color_button)
        self.color_label = QLabel("")
        color_button.clicked.connect(self.onpresscolor)


        # Radio Buttons to be used for target shape
        cross = QRadioButton("Large Crosshair")
        s_cross = QRadioButton("Small Crosshair")
        m_cross = QRadioButton("Maltese Cross")
        square_out = QRadioButton("Square Outline")
        square = QRadioButton("Square")
        circle = QRadioButton("Circle")
        twinkle = QRadioButton("Twinkle")
        self.test_label = QLabel("")

        # Adding the radio buttons to the shape widget
        fix_shape.addWidget(cross)
        fix_shape.addWidget(s_cross)
        fix_shape.addWidget(m_cross)
        fix_shape.addWidget(square_out)
        fix_shape.addWidget(square)
        fix_shape.addWidget(circle)
        fix_shape.addWidget(twinkle)

        # What will happen when a specific radio button is called
        cross.toggled.connect(self.onclick)
        s_cross.toggled.connect(self.onclick)
        m_cross.toggled.connect(self.onclick)
        square_out.toggled.connect(self.onclick)
        square.toggled.connect(self.onclick)
        circle.toggled.connect(self.onclick)
        twinkle.toggled.connect(self.onclick)

        # Generate the scroll bar for the size of the fixation target
        fix_size = QHBoxLayout()
        self.size_bar = QSlider(Qt.Horizontal)
        self.label_size = QLabel()
        self.size_bar.setMinimum(1)
        self.size_bar.setMaximum(20)
        self.size_bar.setValue(5)
        self.size_bar.setTickPosition(QSlider.TicksBelow)
        self.size_bar.setTickInterval(1)
        self.label_size.setText(str(self.size_bar.value()))
        self.size_bar.valueChanged.connect(self.sizechange)

        # Add scroll bar and label to the main widget
        fix_size.addWidget(self.label_size)
        fix_size.addWidget(QLabel(""))
        fix_size.addWidget(self.size_bar)

        # Add all the other widgets to the main layout and set priority
        # layout2.addRow("Color:", QLineEdit())
        layout2.addRow(self.color_layout)
        layout2.addRow(self.color_label)
        layout2.addRow(QLabel(""))
        layout2.addRow(QLabel("Shape:"), fix_shape)  # Adds the radio buttons for the shape to the main layout
        layout2.addRow(self.test_label)
        layout2.addRow(QLabel(""))
        layout2.addRow(QLabel("Size:"), fix_size)
        self.setTabText(1, "Fixation Target Control")
        self.tab2.setLayout(layout2)

    # Slot for the shape of the fixation target being completed
    def onclick(self):
        button = self.sender()
        if button.isChecked():
            # Will be changed to what each shape will look like in the future
            self.test_label.setText("You pressed the button called: " + button.text())

    # Slot for displaying the value of the fixation target as it moves
    def sizechange(self):
        txt = str(self.size_bar.value())
        self.label_size.setText(txt)

    def onpresscolor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_label.setText("Current Color selected: " + str(color.name()))

    # Function for the UI of Tab 3 - Image Calibration Control
    def tab3ui(self):
        layout3 = QFormLayout()

        # Generate buttons needed for image calibration control
        self.load_bg_image_button = QPushButton()
        self.load_bg_image_button.setText("Load Background Image") #Open file explore and select image
        self.image_cal_button = QPushButton()
        self.image_cal_button.setText("Start Image Calibration")
        center_fovea_button = QPushButton()
        center_fovea_button.setText("Center Fovea")

        # Add the image calibration button to its slot when pressed
        self.image_cal_button.clicked.connect(self.onpresscal)
        self.load_bg_image_button.clicked.connect(self.onpressload)

        # Add all the widgets to the main layout and set priority
        layout3.addRow(self.load_bg_image_button)
        layout3.addRow(self.image_cal_button)
        layout3.addRow(center_fovea_button)

        self.setTabText(2, "Image Calibration Control")
        self.tab3.setLayout(layout3)

    def onpresscal(self):
        button = self.sender()
        txt = str(button.text())
        match txt:
            case "Start Image Calibration":
                self.image_cal_button.setText("Select 1st Point on Image")
            case "Select 1st Point on Image":
                self.image_cal_button.setText("Select Corresponding Point (1st Point)")
            case "Select Corresponding Point (1st Point)":
                self.image_cal_button.setText("Select 2nd Point on Image")
            case "Select 2nd Point on Image":
                self.image_cal_button.setText("Select Corresponding Point (2nd Point)")
            case "Select Corresponding Point (2nd Point)":
                self.image_cal_button.setText("Select 3rd Point on Image")
            case "Select 3rd Point on Image":
                self.image_cal_button.setText("Select Corresponding Point (3rd Point)")
            case "Select Corresponding Point (3rd Point)":
                self.image_cal_button.setText("Start Calibration")
            case "Start Calibration":
                self.image_cal_button.setText("New Calibration")
            case "New Calibration":
                self.image_cal_button.setText("Start Image Calibration")
            case _:
                self.image_cal_button.setText("Something went wrong!!!!")

    def onpressload(self):
        button = self.sender()

    # Function for the UI of Tab 4 - Protocol Control
    def tab4ui(self):
        layout4 = QFormLayout()

        # Generate buttons needed for protocol control
        load_p_button = QPushButton()
        load_p_button.setText("Load Protocol") # Need an advance button
        save_p_button = QPushButton()
        save_p_button.setText("Save Protocol")

        # Add all the widgets to the main layout and set priority
        layout4.addRow(load_p_button)  # Should mark locations with size of FOV on display screen
        layout4.addRow(save_p_button)

        self.setTabText(3, "Protocol Control")
        self.tab4.setLayout(layout4)

    # Function for the UI of Tab 5 - Help
    def tab5ui(self):
        layout5 = QFormLayout()
        # Add all the widgets to the main layout and set priority
        layout5.addRow("Help:", QLineEdit())
        self.setTabText(4, "Help")
        self.tab5.setLayout(layout5)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Tabs()
    widget.resize(800, 800)
    widget.show()

    sys.exit(app.exec())
