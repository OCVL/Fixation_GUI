from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtCore
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QTabWidget, QWidget, QFormLayout, QLineEdit, \
    QHBoxLayout, QRadioButton, QSlider, QAbstractSlider

print(PySide6.__version__)  # Prints the pyside6 version
print(PySide6.QtCore.__version__)  # Prints Qt version used to compile Pyside6


class Tabs(QTabWidget):
    def __init__(self, parent=None):
        super(Tabs, self).__init__(parent)

        # Generate the Tabs for the window to hold the settings
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()

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

        # Generate the radio button for fixation target shape
        fix_shape = QHBoxLayout()
        fix_shape.addWidget(QRadioButton("Crosshair"))
        fix_shape.addWidget(QRadioButton("Circle"))
        fix_shape.addWidget(QRadioButton("Square"))

        # Generate the scroll bar for the size of the fixation target
        fix_size = QHBoxLayout()
        size_bar = QSlider(Qt.Horizontal)
        label_size = QLabel()
        size_bar.setMinimum(1)
        size_bar.setMaximum(20)
        size_bar.setValue(5)
        size_bar.setTickPosition(QSlider.TicksBelow)
        size_bar.setTickInterval(1)
        # Need to figure out how to get it to update when value is changed
        size_bar.valueChanged.connect(label_size.setText(str(size_bar.value())))

        # Add scroll bar and label to the main widget
        fix_size.addWidget(label_size)
        fix_size.addWidget(size_bar)

        # Add all the other widgets to the main layout and set priority
        layout2.addRow("Color:", QLineEdit())
        layout2.addRow(QLabel("Shape:"), fix_shape)  # Adds the radio buttons for the shape to the main layout
        layout2.addRow(QLabel("Size:"), fix_size)
        self.setTabText(1, "Fixation Target Control")
        self.tab2.setLayout(layout2)

    # Function for the UI of Tab 3 - Image Calibration Control
    def tab3ui(self):
        layout3 = QFormLayout()

        # Add all the widgets to the main layout and set priority
        layout3.addRow("Load Background Image:", QLineEdit())
        layout3.addRow("Center Fovea:", QLineEdit())
        layout3.addRow("Start Image Calibration:", QLineEdit())
        self.setTabText(2, "Image Calibration Control")
        self.tab2.setLayout(layout3)

    # Function for the UI of Tab 4 - Protocol Control
    def tab4ui(self):
        layout4 = QFormLayout()

        # Add all the widgets to the main layout and set priority
        layout4.addRow("Load Protocol:", QLineEdit())  # Should mark locations with size of FOV on display screen
        layout4.addRow("Save Protocol", QLineEdit())

        self.setTabText(3, "Protocol Control")
        self.tab2.setLayout(layout4)

    # Function for the UI of Tab 5 - Help
    def tab5ui(self):
        layout5 = QFormLayout()

        # Add all the widgets to the main layout and set priority
        layout5.addRow("Load Background Image:", QLineEdit())
        self.setTabText(4, "Help")
        self.tab2.setLayout(layout5)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Tabs()
    widget.resize(600, 800)
    widget.show()

    sys.exit(app.exec())
