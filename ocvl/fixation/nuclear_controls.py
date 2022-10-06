import configparser
from tkinter import filedialog
from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtCore
import sys
import cv2
from PySide6.QtGui import *
from PySide6.QtCore import Qt, QSize, QPointF
from PySide6.QtWidgets import *
from ocvl.fixation.nuclear_info import NuclearInfo


class Tabs(QTabWidget):
    """
    Main class for the control panel that contains various tabs, each with different functionality
    """

    def __init__(self,  eye=None, sub_id=None, save_loc=None, device=None, config_name="C:\\Users\\6262BrennaB\\Desktop\\FixationGUI\\ocvl\\fixation\\test_settings.ini", parent=None):
        """
        Initialization of the class variables
        """
        super(Tabs, self).__init__(parent)

        # All the self class variables to be used in the various tabs
        self.subject_view = None
        self.anatomical_view = None
        self.dim = None
        self.grid_size_default_3 = None
        self.grid_size_default_2 = None
        self.grid_size_default_1 = None
        self.grid_defaults = None
        self.grid_display_save = None
        self.savior_FOVs = None
        self.dim_select = None
        self.FOV_menu = None
        self.info = None
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
        self.label_size = None
        self.test_label = None
        self.size_bar = None
        self.image_cal_button = None
        self.load_bg_image_button = None
        self.eye = eye
        self.sub_id = sub_id
        self.save_loc = save_loc
        self.device = device

        # Load the config file
        self.config = configparser.ConfigParser()
        self.config.read(config_name)

        # Generate the Tabs for the window to hold the settings
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.tab7 = QWidget()
        self.tab8 = QWidget()

        # Set the position of the tabs to be on the right
        self.setTabPosition(QTabWidget.East)

        # Add the tabs generated to the parent window
        self.addTab(self.tab1, "GUI Configuration")
        self.addTab(self.tab2, "Savior Control")
        self.addTab(self.tab3, "Grid Configuration")
        self.addTab(self.tab4, "Target Control")
        self.addTab(self.tab5, "Planed Protocol")
        self.addTab(self.tab6, "Image Calibration")
        self.addTab(self.tab7, "Stimulus Control")
        self.addTab(self.tab8, "Help")

        # Make a UI function for each of the tabs
        self.stimControlTab()
        self.fixationTargetControlTab()
        self.imCalibrationControlTab()
        self.protocolControlTab()
        self.helpTab()
        self.infoTab()
        self.saviorControlTab()
        self.gridConfigurationTab()

        # UI functions for the new tab layout
        self.guiSetUp()
        # self.imagingTab()
        # self.sessionReview()

        # Set the Title of the Window
        self.setWindowTitle("Control Settings")

    def guiSetUp(self):
        layout = QFormLayout()
        grid_config_group = QGroupBox("Grid Configuration")
        grid_setup_layout = QVBoxLayout()

        # Labels for each Grid section
        quick_size_label = QLabel("Quick Sizes:")
        dim_menu_label = QLabel("Grid Dimension:")

        # Default button size creation
        self.grid_defaults = self.config.get("test", "grid_size_defaults").split("/")
        self.grid_size_default_1 = QRadioButton(self.grid_defaults[0])
        self.grid_size_default_2 = QRadioButton(self.grid_defaults[1])
        self.grid_size_default_3 = QRadioButton(self.grid_defaults[2])

        # Connect the buttons to the slots
        self.grid_size_default_1.toggled.connect(self.gridSizeChange)
        self.grid_size_default_2.toggled.connect(self.gridSizeChange)
        self.grid_size_default_3.toggled.connect(self.gridSizeChange)

        # Add the buttons to the layout
        grid_setup_layout.addWidget(quick_size_label)
        grid_setup_layout.addWidget(self.grid_size_default_1)
        grid_setup_layout.addWidget(self.grid_size_default_2)
        grid_setup_layout.addWidget(self.grid_size_default_3)

        # Set up the other sizes in the dropdown menu
        self.dim_select = QComboBox()

        # Add all the different possible dims for grid
        for x in range(10, 61, 5):
            self.dim_select.addItem(str(x) + "x" + str(x))

        # Connect the dropdown menus (grid dims) to their slots
        self.dim_select.currentTextChanged.connect(self.GridSizeChange)

        # Default from config file
        self.dim = self.config.get("test", "grid_size_start_default")
        self.dim_select.setCurrentIndex(self.dim_select.findText(self.dim))

        # Add the dropdown and its label to the layout
        grid_setup_layout.addWidget(dim_menu_label)
        grid_setup_layout.addWidget(self.dim_select)

        # Swap the view of T/N labels
        view_layout = QHBoxLayout()
        self.anatomical_view = QRadioButton("Anatomical View")
        self.subject_view = QRadioButton("Subject View")

        # Connect the View Radio buttons to the slot
        self.anatomical_view.toggled.connect(self.viewChange)
        self.subject_view.toggled.connect(self.viewChange)

        # Add view buttons to their layout and the main
        view_layout.addWidget(self.anatomical_view)
        view_layout.addWidget(self.subject_view)

        # Add view buttons to the layout
        grid_setup_layout.addLayout(view_layout)

        # Add the grid layout to the Group layout
        grid_config_group.setLayout(grid_setup_layout)

        layout.addRow(grid_config_group)

        # Load Protocol Set up stuff
        protocol_config_group = QGroupBox("Protocol")
        protocol_layout = QVBoxLayout()

        # Make the load Protocol button and its corresponding label
        self.load_p_button = QPushButton()
        self.load_p_button.setText("Load Protocol")  # Need an advance button
        self.load_p_label = QLabel()

        # Add the slot to the button and add the button and the layout to the group layout
        self.load_p_button.clicked.connect(self.onPressLoadP)
        protocol_layout.addWidget(self.load_p_button)  # Should mark locations with size of FOV on display screen
        protocol_layout.addWidget(self.load_p_label)

        # Add the protocol layout to the group layout
        protocol_config_group.setLayout(protocol_layout)
        layout.addRow(protocol_config_group)

        # Image Calibration Group
        image_config_group = QGroupBox("Image Calibration")
        image_cal_layout = QHBoxLayout()

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
        self.image_cal_button.clicked.connect(self.onPressCal)
        self.load_bg_image_button.clicked.connect(self.onPressLoad)

        # Add all the widgets to the main layout and set priority
        image_cal_layout.addWidget(self.load_bg_image_button)
        image_cal_layout.addWidget(self.image_cal_button)
        image_cal_layout.addWidget(center_fovea_button)
        image_cal_layout.addRow(self.image_label)

        # Add the protocol layout to the group layout
        image_config_group.setLayout(image_cal_layout)
        layout.addRow(image_config_group)

        self.tab1.setLayout(layout)

    def stimControlTab(self):  # Currently Complete
        """
        Function for the UI properties and functionality of Tab 1 - Stimulus control
        """
        layout = QFormLayout()
        layout.addRow("Port Number:", QLineEdit())
        layout.addRow(QLabel(""))
        layout.addRow(QLabel("Stimulus Parameters:"))
        layout.addRow("Frequency: ", QLineEdit())
        layout.addRow("Duration", QLineEdit())
        layout.addRow("Start Time", QLineEdit())
        layout.addRow("Frames After", QLineEdit())

        # self.setTabText(0, "Stimulus Control")
        self.tab7.setLayout(layout)

    def fixationTargetControlTab(self):
        """
        Function for the UI properties and functionality of Tab 2 - Fixation Target Control
        """
        layout = QFormLayout()

        # Widget for the shape objects for the fixation target
        fix_shape = QHBoxLayout()
        color_shape = QHBoxLayout()

        # Color wheel for selecting the color of the target
        self.color_layout = QHBoxLayout()
        color_button = QPushButton("Select Color")
        self.color_layout.addWidget(color_button)
        self.color_name_label = QLabel("")
        self.color_display_label = QLabel()
        color_button.clicked.connect(self.onPressColor)

        # Push Buttons to be used for target shape
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
        self.drawTargets()

        # Adding the radio buttons to the shape widget
        fix_shape.addWidget(self.cross)
        fix_shape.addWidget(self.s_cross)
        fix_shape.addWidget(self.m_cross)
        fix_shape.addWidget(self.square_out)
        fix_shape.addWidget(self.square)
        fix_shape.addWidget(self.circle)
        fix_shape.addWidget(self.twinkle)

        # What will happen when a specific radio button is called
        self.cross.clicked.connect(self.onClick)
        self.s_cross.clicked.connect(self.onClick)
        self.m_cross.clicked.connect(self.onClick)
        self.square_out.clicked.connect(self.onClick)
        self.square.clicked.connect(self.onClick)
        self.circle.clicked.connect(self.onClick)
        self.twinkle.clicked.connect(self.onClick)

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
        self.size_bar.valueChanged.connect(self.sizeChange)

        # Add scroll bar and label to the main widget
        fix_size.addWidget(self.label_size)
        fix_size.addWidget(QLabel(""))
        fix_size.addWidget(self.size_bar)

        # Add all the Color related widgets to their layout
        color_shape.addWidget(self.color_name_label)
        color_shape.addWidget(self.color_display_label)

        # Generate the Radio buttons for the target being on/off
        target_display_bttns = QHBoxLayout()
        self.target_on_bttn = QRadioButton("On")
        self.target_off_bttn = QRadioButton("Off")

        # Connect the radio button to their slot
        self.target_on_bttn.toggled.connect(self.displayTarget)
        self.target_off_bttn.toggled.connect(self.displayTarget)

        # Add the radio buttons to their layout
        target_display_bttns.addWidget(self.target_on_bttn)
        target_display_bttns.addWidget(self.target_off_bttn)

        layout.addRow(self.color_layout)
        layout.addRow(color_shape)
        layout.addRow(QLabel(""))
        layout.addRow(QLabel("Shape:"))
        layout.addRow(fix_shape)  # Adds the radio buttons for the shape to the main layout
        layout.addRow(self.test_label)
        layout.addRow(QLabel(""))
        layout.addRow(QLabel("Size:"), fix_size)
        layout.addRow("Fixation target Display:", target_display_bttns)

        # self.setTabText(1, "Fixation Target Control")
        self.tab4.setLayout(layout)

    def imCalibrationControlTab(self):
        """
        Function for the UI properties and functionality of Tab 3 - Image Calibration Control
        """
        layout3 = QFormLayout()

        # # Attributes needed to display an image
        # self.image_label = QLabel("")
        # self.image_label.resize(500, 500)
        #
        # # Generate buttons needed for image calibration control
        # self.load_bg_image_button = QPushButton()
        # self.load_bg_image_button.setText("Load Background Image")  # Open file explore and select image
        # self.image_cal_button = QPushButton()
        # self.image_cal_button.setText("Start Image Calibration")
        # center_fovea_button = QPushButton()
        # center_fovea_button.setText("Center Fovea")
        #
        # # Add the image calibration button to its slot when pressed
        # self.image_cal_button.clicked.connect(self.onPressCal)
        # self.load_bg_image_button.clicked.connect(self.onPressLoad)
        #
        # # Add all the widgets to the main layout and set priority
        # layout3.addRow(self.load_bg_image_button)
        # layout3.addRow(self.image_label)
        # layout3.addRow(self.image_cal_button)
        # layout3.addRow(center_fovea_button)

        # self.setTabText(2, "Image Calibration Control")
        self.tab6.setLayout(layout3)

    def protocolControlTab(self):
        """
        Function for the UI properties and functionality of Tab 4 - Protocol Control
        """
        layout4 = QFormLayout()

        # Generate buttons needed for protocol control
        # self.load_p_button = QPushButton()
        # self.load_p_button.setText("Load Protocol")  # Need an advance button
        # self.load_p_label = QLabel()
        self.save_p_button = QPushButton()
        self.save_p_button.setText("Advance")
        self.save_p_label = QLabel()

        # Add the protocol buttons to their slots
        # self.load_p_button.clicked.connect(self.onPressLoadP)
        self.save_p_button.clicked.connect(self.onPressAdvanceP)

        # Add all the widgets to the main layout and set priority
        # layout4.addRow(self.load_p_button)  # Should mark locations with size of FOV on display screen
        # layout4.addRow(self.load_p_label)
        layout4.addRow(self.save_p_button)
        layout4.addRow(self.save_p_label)

        # self.setTabText(3, "Protocol Control")
        self.tab5.setLayout(layout4)

    def helpTab(self):
        """
        Function for the UI properties and functionality of Tab 5 - Help and Hot Key Shortcuts
        """
        layout5 = QFormLayout()
        # Add all the widgets to the main layout and set priority
        layout5.addRow(QLabel("Help:"))
        layout5.addRow(QLabel("F4 - Record a Video"))

        # self.setTabText(4, "Help")
        self.tab8.setLayout(layout5)

    def infoTab(self):
        self.info = NuclearInfo(self.eye, self.sub_id, self.save_loc, self.device)
        layout = QFormLayout()
        layout.addWidget(self.info)
        # self.tab1.setLayout(layout)

    def saviorControlTab(self):
        layout = QFormLayout()
        layout.addRow("Number of Frames:", QLineEdit())

        self.FOV_menu = QComboBox()

        # get the FOVs from the config file
        self.savior_FOVs = self.config.get("test", "savior_FOVs").split("/")

        # adds all the FOVs in the list
        for x in self.savior_FOVs:
            self.FOV_menu.addItem(x)

        # sets the selection to the first one
        self.FOV_menu.setCurrentIndex(0)

        layout.addRow("Current FOV:", self.FOV_menu)
        self.tab2.setLayout(layout)

    def gridConfigurationTab(self):
        layout = QFormLayout()
        # button_layout = QHBoxLayout()

        # # Drop downs for the 2 dims
        # self.horz_dim_select = QComboBox()
        # self.vert_dim_select = QComboBox()

        # # Defualt button size creation
        # self.grid_defaults = self.config.get("test", "grid_size_defaults").split("/")
        # self.grid_size_default_1 = QRadioButton(self.grid_defaults[0])
        # self.grid_size_default_2 = QRadioButton(self.grid_defaults[1])
        # self.grid_size_default_3 = QRadioButton(self.grid_defaults[2])

        # # Connect the buttons to the slot
        # self.grid_size_default_1.toggled.connect(self.gridSizeChange)
        # self.grid_size_default_2.toggled.connect(self.gridSizeChange)
        # self.grid_size_default_3.toggled.connect(self.gridSizeChange)

        # # Add the Radio Buttons to the button layout
        # button_layout.addWidget(self.grid_size_default_1)
        # button_layout.addWidget(self.grid_size_default_2)
        # button_layout.addWidget(self.grid_size_default_3)

        # # Add all the different possible dims to each the vert and horz spacing for grid
        # for x in range(10, 61, 5):
        #     self.horz_dim_select.addItem(str(x))
        #     self.vert_dim_select.addItem(str(x))
        #
        # # Connect the drop down menues (grid dims) to their slots
        # self.horz_dim_select.currentTextChanged.connect(self.horzGridSizeChange)
        # self.vert_dim_select.currentTextChanged.connect(self.vertGridSizeChange)
        #
        # # Default from config file
        # [self.horz_dim, self.vert_dim] = self.config.get("test", "grid_size_start_default").split("x")
        # self.horz_dim_select.setCurrentIndex(self.horz_dim_select.findText(self.horz_dim))
        # self.vert_dim_select.setCurrentIndex(self.vert_dim_select.findText(self.vert_dim))

        # layout.addRow("Quick Sizes (degrees):", button_layout)
        # layout.addRow("Horizontal Grid Dim:", self.horz_dim_select)
        # layout.addRow('Vertical Grid Dim:', self.vert_dim_select)

        # Reference Point / reset button
        self.ref_pt_button = QPushButton()
        self.ref_pt_button.setText("Set Reference Point")
        self.ref_pt_label = QLabel("")

        # Connect the reference point button to its slot
        self.ref_pt_button.clicked.connect(self.referencePointBttnClicked)

        # Add the Reference button and label to the main layout
        layout.addRow(QLabel(""))
        layout.addRow(self.ref_pt_button)
        layout.addRow(self.ref_pt_label)

        # # Swap the view of T/N labels
        # view_layout = QHBoxLayout()
        # self.anatomical_view = QRadioButton("Anatomical View")
        # self.subject_view = QRadioButton("Subject View")
        #
        # # Connect the View Radio buttons to the slot
        # self.anatomical_view.toggled.connect(self.viewChange)
        # self.subject_view.toggled.connect(self.viewChange)
        #
        # # Add view buttons to their layout and the main
        # view_layout.addWidget(self.anatomical_view)
        # view_layout.addWidget(self.subject_view)
        # layout.addRow(view_layout)

        # Save current grid push button
        self.grid_display_save = QPushButton()
        self.grid_display_save.setText("Save Current Grid Display")

        # Connect to the slot and add to main layout
        self.grid_display_save.clicked.connect(self.saveGrid)
        layout.addRow(QLabel(""))
        layout.addRow(self.grid_display_save)

        self.tab3.setLayout(layout)

    """
    Functions below are used in the UI for fixationTargetControlTab
    """

    def drawTargets(self):
        """
        Function that calls each function in charge of drawing on the fixation target to be selected
        """
        # Call the functions to draw the different targets
        self.drawCross()
        self.drawSmallCross()
        self.drawSqaure()
        self.drawSquareOutline()
        self.drawCircle()
        self.drawTwinkle()
        self.drawMaltcross()

    def drawCross(self):
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

    def drawSmallCross(self):
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

    def drawSqaure(self):
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

    def drawSquareOutline(self):
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

    def drawCircle(self):
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

    def drawTwinkle(self):
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

    def drawMaltcross(self):
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
    Slots that are used in the UI for fixationTargetControlTab
    """

    def onClick(self):
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

    def sizeChange(self):
        """
        Slot for displaying the size of the fixation target as it moves
        """
        txt = str(self.size_bar.value())
        self.label_size.setText(txt)

    def onPressColor(self):
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

            self.drawTargets()

    """
    Slots that are used in the UI for imCalibrationControlTab
    """

    def onPressCal(self):
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

    def onPressLoad(self):
        button = self.sender()
        image_path = filedialog.askopenfilenames(title='Select the background image', filetypes=[
            ("image", ".jpeg"),
            ("image", ".png"),
            ("image", ".jpg"),
            ("image", ".tif")])
        print(image_path)
        self.image_label.setText(str(image_path))

    """
    Slots that are used in the UI for protocolControlTab
    """

    def onPressLoadP(self):
        button = self.sender()
        protocol_path = filedialog.askopenfilenames(title='Select the protocol to load', filetypes=[
            ("protocol", ".csv")])
        print(protocol_path)
        self.load_p_label.setText(str(protocol_path))

    def onPressAdvanceP(self):
        button = self.sender()
        txt = self.save_p_label.text()
        match txt:
            case "Button has been clicked":
                self.save_p_label.setText("")
            case _:
                self.save_p_label.setText("Button has been clicked")

    """
    slots for the Grid Configuration Tab
    """

    def gridSizeChange(self):
        """
        Slot for the grid default quick sizes to be changed
        :return:
        """
        button = self.sender()
        txt = button.text()
        if button.isChecked():
            print("Pressed the button called: " + txt)
            v1 = str(self.grid_defaults[0])
            v2 = str(self.grid_defaults[1])
            v3 = str(self.grid_defaults[2])
            if txt == v1:
                self.dim = self.grid_defaults[0]
                self.dim_select.setCurrentIndex(self.dim_select.findText(self.dim))
            elif txt == v2:
                self.dim = self.grid_defaults[0]
                self.dim_select.setCurrentIndex(self.dim_select.findText(self.dim))
            elif txt == v3:
                self.dim = self.grid_defaults[0]
                self.dim_select.setCurrentIndex(self.dim_select.findText(self.dim))
            else:
                print("Something went wrong!")

    def GridSizeChange(self):
        """
        Slot for the horizontal drop down menu for the grid sizes
        :return:
        """
        self.dim = self.dim_select.currentText()
        print(self.dim)

    # def vertGridSizeChange(self):
    #     """
    #     Slot for the horizontal drop down menu for the grid sizes
    #     :return:
    #     """
    #     self.vert_dim = self.vert_dim_select.currentText()
    #     print(self.vert_dim)

    def referencePointBttnClicked(self):
        """
        Slot for the reference button to change based off the when it was last clicked
        :return:
        """
        button = self.sender()
        txt = str(button.text())
        match txt:
            case "Set Reference Point":
                # Add a label to display what was selected as the current reference point
                self.ref_pt_label.setText("Reference Point (x,y)")
                self.ref_pt_button.setText("Clear Reference Point")
            case "Clear Reference Point":
                self.ref_pt_button.setText("Set Reference Point")
            case _:
                print("Something went wrong!")

    def viewChange(self):
        """
        Slot for the view of the labels on the grid to be swaped Temp/Nas
        :return:
        """
        button = self.sender()
        txt = button.text()
        if button.isChecked():
            print("Pressed the button called: " + txt)

    def saveGrid(self):
        """
        Slot for the save grid display button
        :return:
        """
        button = self.sender()
        print(button.text())

    def displayTarget(self):
        """
        Slot for if the fixation target is displayed to the subject
        :return:
        """
        button = self.sender()
        if button.isChecked():
            txt = button.text()
            print(txt)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Tabs()
    widget.resize(800, 800)
    widget.show()

    sys.exit(app.exec())
