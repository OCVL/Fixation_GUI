from tkinter import filedialog
from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtCore
import sys
import cv2
from PySide6.QtGui import *
from PySide6.QtCore import Qt, QSize, QPointF
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QTabWidget, QWidget, QFormLayout, QLineEdit, \
    QHBoxLayout, QRadioButton, QSlider, QAbstractSlider, QPushButton, QColorDialog, QVBoxLayout, QComboBox, \
    QGraphicsColorizeEffect

# print(PySide6.__version__)  # Prints the pyside6 version
# print(PySide6.QtCore.__version__)  # Prints Qt version used to compile Pyside6


class Tabs(QTabWidget):
    def __init__(self, parent=None):
        """
        Initialization of the class variables
        """
        super(Tabs, self).__init__(parent)

        # Generate the Tabs for the window to hold the settings
        self.stim_wavelengths = None
        self.save_p_label = None
        self.save_p_button = None
        self.load_p_label = None
        self.load_p_button = None
        self.custom_color = QtGui.QColor('green')
        self.image_label = None
        self.twinkle = None
        self.circle = None
        self.square = None
        self.m_cross = None
        self.square_out = None
        self.s_cross = None
        self.cross = None
        self.color_display_label = None
        self.color_name_label = None
        self.color_layout = None
        self.graphic = None
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

    def tab1ui(self):
        """
        Function for the UI properties and functionality of Tab 1 - Stimulus control
        """
        layout1 = QFormLayout()
        layout1.addRow("Port Number:", QLineEdit())
        layout1.addRow(QLabel(""))
        layout1.addRow(QLabel("Stimulus Parameters:"))
        layout1.addRow("Frequency: ", QLineEdit())
        layout1.addRow("Duration", QLineEdit())
        layout1.addRow("Start Time", QLineEdit())
        layout1.addRow("Frames After", QLineEdit())

        self.setTabText(0, "Stimulus Control")
        self.tab1.setLayout(layout1)

    def tab2ui(self):
        """
        Function for the UI properties and functionality of Tab 2 - Fixation Target Control
        """
        layout2 = QFormLayout()

        # Widget for the shape objects for the fixation target
        fix_shape = QHBoxLayout()
        color_shape = QHBoxLayout()

        # Color wheel for selecting the color of the target
        self.color_layout = QHBoxLayout()
        color_button = QPushButton("Select Color")
        self.color_layout.addWidget(color_button)
        self.color_name_label = QLabel("")
        self.color_display_label = QLabel()
        color_button.clicked.connect(self.onpresscolor)

        # Radio Buttons to be used for target shape
        self.cross = QPushButton("Large Crosshair")
        self.s_cross = QPushButton("Small Crosshair")
        self.m_cross = QPushButton("Maltese Cross")
        self.square_out = QPushButton("Square Outline")
        self.square = QPushButton("Square")
        self.circle = QPushButton("Circle")
        self.twinkle = QPushButton("Twinkle")
        self.test_label = QLabel("")

        # Change the shape of the buttons to be squares
        self.cross.setFixedSize(QSize(25, 25))
        self.s_cross.setFixedSize(QSize(25, 25))
        self.m_cross.setFixedSize(QSize(25, 25))
        self.square_out.setFixedSize(QSize(25, 25))
        self.square.setFixedSize(QSize(25, 25))
        self.circle.setFixedSize(QSize(25, 25))
        self.twinkle.setFixedSize(QSize(25, 25))

        # Call the functions to draw the different targets
        self.drawtargets()

        # Adding the radio buttons to the shape widget
        fix_shape.addWidget(self.cross)
        fix_shape.addWidget(self.s_cross)
        fix_shape.addWidget(self.m_cross)
        fix_shape.addWidget(self.square_out)
        fix_shape.addWidget(self.square)
        fix_shape.addWidget(self.circle)
        fix_shape.addWidget(self.twinkle)

        # What will happen when a specific radio button is called
        self.cross.clicked.connect(self.onclick)
        self.s_cross.clicked.connect(self.onclick)
        self.m_cross.clicked.connect(self.onclick)
        self.square_out.clicked.connect(self.onclick)
        self.square.clicked.connect(self.onclick)
        self.circle.clicked.connect(self.onclick)
        self.twinkle.clicked.connect(self.onclick)

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
        color_shape.addWidget(self.color_name_label)
        color_shape.addWidget(self.color_display_label)
        layout2.addRow(self.color_layout)
        layout2.addRow(color_shape)
        layout2.addRow(QLabel(""))
        layout2.addRow(QLabel("Shape:"))
        layout2.addRow(fix_shape)  # Adds the radio buttons for the shape to the main layout
        layout2.addRow(self.test_label)
        layout2.addRow(QLabel(""))
        layout2.addRow(QLabel("Size:"), fix_size)
        self.setTabText(1, "Fixation Target Control")
        self.tab2.setLayout(layout2)

    def tab3ui(self):
        """
        Function for the UI properties and functionality of Tab 3 - Image Calibration Control
        """
        layout3 = QFormLayout()

        # Attributes needed to display an image
        self.image_label = QLabel("")
        self.image_label.resize(500, 500)

        # Generate buttons needed for image calibration control
        self.load_bg_image_button = QPushButton()
        self.load_bg_image_button.setText("Load Background Image")  # Open file explore and select image
        self.image_cal_button = QPushButton()
        self.image_cal_button.setText("Start Image Calibration")
        center_fovea_button = QPushButton()
        center_fovea_button.setText("Center Fovea")

        # Add the image calibration button to its slot when pressed
        self.image_cal_button.clicked.connect(self.onpresscal)
        self.load_bg_image_button.clicked.connect(self.onpressload)

        # Add all the widgets to the main layout and set priority
        layout3.addRow(self.load_bg_image_button)
        layout3.addRow(self.image_label)
        layout3.addRow(self.image_cal_button)
        layout3.addRow(center_fovea_button)

        self.setTabText(2, "Image Calibration Control")
        self.tab3.setLayout(layout3)

    def tab4ui(self):
        """
        Function for the UI properties and functionality of Tab 4 - Protocol Control
        """
        layout4 = QFormLayout()

        # Generate buttons needed for protocol control
        self.load_p_button = QPushButton()
        self.load_p_button.setText("Load Protocol")  # Need an advance button
        self.load_p_label = QLabel()
        self.save_p_button = QPushButton()
        self.save_p_button.setText("Save Protocol")
        self.save_p_label = QLabel()

        # Add the protocol buttons to their slots
        self.load_p_button.clicked.connect(self.onpressloadp)
        self.save_p_button.clicked.connect(self.onpresssavep)

        # Add all the widgets to the main layout and set priority
        layout4.addRow(self.load_p_button)  # Should mark locations with size of FOV on display screen
        layout4.addRow(self.load_p_label)
        layout4.addRow(self.save_p_button)
        layout4.addRow(self.save_p_label)

        self.setTabText(3, "Protocol Control")
        self.tab4.setLayout(layout4)

    def tab5ui(self):
        """
        Function for the UI properties and functionality of Tab 5 - Help and Hot Key Shortcuts
        """
        layout5 = QFormLayout()
        # Add all the widgets to the main layout and set priority
        layout5.addRow(QLabel("Help:"))
        layout5.addRow(QLabel("F4 - Record a Video"))
        self.setTabText(4, "Help")
        self.tab5.setLayout(layout5)

    """
    Functions below are used in the UI for Tab 2
    """

    def drawtargets(self):
        """
        Function that calls each function in charge of drawing on the fixation target to be selected
        """
        # Call the functions to draw the different targets
        self.drawcross()
        self.drawsmallcross()
        self.drawsqaure()
        self.drawsquareoutline()
        self.drawcircle()
        self.drawtwinkle()
        self.drawmaltcross()

    def drawcross(self):
        canvas = QtGui.QPixmap(QSize(100, 100))
        canvas.fill(Qt.black)
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen(self.custom_color, 10)
        painter.setPen(pen)
        painter.drawLine(10, 50, 90, 50)
        painter.drawLine(50, 10, 50, 90)
        painter.end()
        self.cross.setIcon(canvas)
        self.cross.setIconSize(QSize(100, 100))
        self.cross.setStyleSheet("text-align: left;")

    def drawsmallcross(self):
        canvas = QtGui.QPixmap(QSize(100, 100))
        canvas.fill(Qt.black)
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen(self.custom_color, 10)
        painter.setPen(pen)
        painter.drawLine(35, 50, 65, 50)
        painter.drawLine(50, 35, 50, 65)
        painter.end()
        self.s_cross.setIcon(canvas)
        self.s_cross.setIconSize(QSize(100, 100))
        self.s_cross.setStyleSheet("text-align: left;")

    def drawsqaure(self):
        canvas = QtGui.QPixmap(QSize(100, 100))
        canvas.fill(Qt.black)
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen(self.custom_color, 10)
        painter.setPen(pen)
        painter.setBrush(self.custom_color)
        painter.drawRect(15, 15, 70, 70)
        painter.end()
        self.square.setIcon(canvas)
        self.square.setIconSize(QSize(100, 100))
        self.square.setStyleSheet("text-align: left;")

    def drawsquareoutline(self):
        canvas = QtGui.QPixmap(QSize(100, 100))
        canvas.fill(Qt.black)
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen(self.custom_color, 10)
        pen = QtGui.QPen(self.custom_color, 10)
        painter.setPen(pen)
        painter.drawLine(20, 20, 20, 80)
        painter.drawLine(20, 20, 80, 20)
        painter.drawLine(80, 20, 80, 80)
        painter.drawLine(20, 80, 80, 80)
        painter.end()
        self.square_out.setIcon(canvas)
        self.square_out.setIconSize(QSize(100, 100))
        self.square_out.setStyleSheet("text-align: left;")

    def drawcircle(self):
        canvas = QtGui.QPixmap(QSize(100, 100))
        canvas.fill(Qt.black)
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen(self.custom_color, 10)
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(self.custom_color))
        center = QPointF(50, 50)
        painter.drawEllipse(center, 35, 35)
        painter.end()
        self.circle.setIcon(canvas)
        self.circle.setIconSize(QSize(100, 100))
        self.circle.setStyleSheet("text-align: left;")

    def drawtwinkle(self):
        canvas = QtGui.QPixmap(QSize(100, 100))
        canvas.fill(Qt.black)
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen(self.custom_color, 10)
        painter.setPen(pen)
        painter.drawLine(35, 50, 65, 50)
        painter.drawLine(15, 50, 15, 50)
        painter.drawLine(85, 50, 85, 50)
        painter.drawLine(50, 35, 50, 65)
        painter.drawLine(50, 85, 50, 85)
        painter.drawLine(50, 15, 50, 15)
        painter.drawLine(25, 25, 75, 75)
        painter.drawLine(75, 25, 25, 75)
        painter.end()
        self.twinkle.setIcon(canvas)
        self.twinkle.setIconSize(QSize(100, 100))
        self.twinkle.setStyleSheet("text-align: left;")

    def drawmaltcross(self):
        canvas = QtGui.QPixmap(QSize(100, 100))
        canvas.fill(Qt.black)
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen(self.custom_color, 5)
        painter.setPen(pen)
        painter.drawLine(30, 10, 70, 90)
        painter.drawLine(70, 10, 30, 90)
        painter.drawLine(10, 30, 90, 70)
        painter.drawLine(10, 70, 90, 30)
        painter.drawLine(50, 25, 30, 10)
        painter.drawLine(50, 25, 70, 10)
        painter.drawLine(50, 75, 30, 90)
        painter.drawLine(50, 75, 70, 90)
        painter.drawLine(25, 50, 10, 70)
        painter.drawLine(25, 50, 10, 30)
        painter.drawLine(75, 50, 90, 70)
        painter.drawLine(75, 50, 90, 30)
        painter.end()
        self.m_cross.setIcon(canvas)
        self.m_cross.setIconSize(QSize(100, 100))
        self.m_cross.setStyleSheet("text-align: left;")

    """
    Slots that are used in the UI for Tab 2
    """
    def onclick(self):
        """
        Slot for the shape of the fixation target to be selected
        """
        button = self.sender()
        txt = str(button.text())
        match txt:
            case "Large Crosshair":
                # Will be changed to what each shape will look like in the future
                self.test_label.setText("You pressed the button called: " + txt)
            case "Small Crosshair":
                # Will be changed to what each shape will look like in the future
                self.test_label.setText("You pressed the button called: " + txt)
            case "Maltese Cross":
                # Will be changed to what each shape will look like in the future
                self.test_label.setText("You pressed the button called: " + txt)
            case "Square Outline":
                # Will be changed to what each shape will look like in the future
                self.test_label.setText("You pressed the button called: " + txt)
            case "Square":
                # Will be changed to what each shape will look like in the future
                self.test_label.setText("You pressed the button called: " + txt)
            case "Circle":
                # Will be changed to what each shape will look like in the future
                self.test_label.setText("You pressed the button called: " + txt)
            case "Twinkle":
                # Will be changed to what each shape will look like in the future
                self.test_label.setText("You pressed the button called: " + txt)

    def sizechange(self):
        """
        Slot for displaying the size of the fixation target as it moves
        """
        txt = str(self.size_bar.value())
        self.label_size.setText(txt)

    def onpresscolor(self):
        """
        Slot used to select the color of the fixation target
        """
        color = QColorDialog.getColor()  # Might want to make a class variable to change the color of the fixation target to the one selected
        self.custom_color = color
        if color.isValid():
            self.color_name_label.setText("Current Color selected: " + str(color.name()))
            self.color_display_label.setGeometry(100, 100, 200, 60)
            self.color_display_label.setStyleSheet("QLabel""{"
                                                   "border : 5px solid black;"
                                                   "background-color: color;"
                                                   "}")
            # setting graphic effect to the label
            self.graphic = QGraphicsColorizeEffect()
            # setting color to the graphic
            self.graphic.setColor(color)
            # setting graphic to the label
            self.color_display_label.setGraphicsEffect(self.graphic)

            self.drawtargets()

    """
    Slots that are used in the UI for Tab 3
    """

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
        image_path = filedialog.askopenfilenames(title='Select the background image', filetypes=[
                    ("image", ".jpeg"),
                    ("image", ".png"),
                    ("image", ".jpg"),
                    ("image", ".tif")])
        print(image_path)
        self.image_label.setText(str(image_path))

    """
    Slots that are used in the UI for Tab 4
    """
    def onpressloadp(self):
        button = self.sender()
        protocol_path = filedialog.askopenfilenames(title='Select the protocol to load', filetypes=[
            ("protocol", ".csv")])
        print(protocol_path)
        self.load_p_label.setText(str(protocol_path))

    def onpresssavep(self):
        button = self.sender()
        txt = self.save_p_label.text()
        match txt:
            case "Button has been clicked":
                self.save_p_label.setText("")
            case _:
                self.save_p_label.setText("Button has been clicked")



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Tabs()
    widget.resize(800, 800)
    widget.show()

    sys.exit(app.exec())
