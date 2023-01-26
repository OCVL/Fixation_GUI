from tkinter import filedialog

import PySide6
from PySide6 import QtWidgets, QtGui, QtCore
import sys
from PySide6.QtGui import *
from PySide6.QtCore import Qt, QSize, QPointF, QEvent
from PySide6.QtWidgets import *


class Tabs(QTabWidget):
    """
    Main class for the control panel that contains various tabs, each with different functionality
    """

    def __init__(self, var, parent=None):
        """
        Initialization of the class variables
        """
        super(Tabs, self).__init__(parent)
        self.none_selected = None
        self.var = var

        # All the self class variables to be used in the various tabs
        self.target_vis_bttn = None
        self.ref_pt_label = None
        self.ref_pt_button = None
        self.MTE = None
        self.TRC = None
        self.TLC = None
        self.MLE = None
        self.BLC = None
        self.MBE = None
        self.BRC = None
        self.MRE = None
        self.CTR = None
        self.grid_vis = None
        self.animation_speed = None
        self.animation = None
        self.vert = None
        self.horz = None
        self.target_off_bttn = None
        self.target_on_bttn = None
        self.subject_view = None
        self.anatomical_view = None
        self.grid_size_default_3 = None
        self.grid_size_default_2 = None
        self.grid_size_default_1 = None
        self.grid_defaults = None
        self.grid_display_save = None
        self.dim_select = None
        self.FOV_menu = None
        self.info = None
        self.save_p_label = None
        self.save_p_button = None
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
        self.n_frames = None

        # getting the default whether the grid is on or not from the config file
        grid_def = int(self.var.config.get("test", "grid_visible"))
        if grid_def == 1:
            self.var.grid_vis = True
        else:
            self.var.grid_vis = False

        # Generate the Tabs for the window to hold the settings
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        # set to no focus to disable the arrow keys moving through the tabs (so they can be used for the target movement)
        self.setFocusPolicy(Qt.NoFocus)

        # Set the position of the tabs to be on the right
        self.setTabPosition(QTabWidget.East)
        self.setTabShape(QTabWidget.Triangular)
        # need to figure out how to resize these appropriately when size of window changes
        self.setMaximumWidth(350)
        self.setMaximumHeight(700)

        # Add the tabs generated to the parent window
        self.addTab(self.tab1, "GUI Configuration")
        self.addTab(self.tab2, "Imaging")
        self.addTab(self.tab3, "Stimulus Control")
        self.addTab(self.tab4, "Session Review")

        # UI functions for the new tab layout
        self.guiSetUp()
        self.imagingTab()
        self.stimControlTab()
        self.sessionReview()

        # Set the Title of the Window
        self.setWindowTitle("Control Settings")

    def guiSetUp(self):
        """
        Function for the UI properties and functionality for the GUI set up tab
        Components:
            - Grid Configuration
                * Quick sizes
                * Grid dimension drop-down
                * Set Reference Point
                * Label (T/N) view - Removed might come back after meeting
            - Protocol
                * Load Protocol button
                * Label with file path with protocol
            - image Calibration
                * Load background image button
                * Calibrate Image button
                * Center Fovea Button
            - Target Setup
                * Color select Button
                * Label with color name and then displays selected color
                * Target Size Label and scroll bar
                * Target Shapes (6 currently)
        :return:
        """
        # Main tab layout
        layout = QFormLayout()

        # Grid Group and needed layouts
        grid_config_group = QGroupBox("Grid Configuration")
        grid_setup_layout = QVBoxLayout()
        quick_size_layout = QHBoxLayout()

        # set to no focus to disable the arrow keys moving through the tabs (so they can be used for the target movement)
        grid_config_group.setFocusPolicy(Qt.NoFocus)

        # Labels for each Grid section
        quick_size_label = QLabel("Quick Sizes:")
        dim_menu_label = QLabel("Grid Dimension:")

        # Default button size creation
        self.grid_defaults = self.var.config.get("test", "grid_size_defaults").split("/")
        self.grid_size_default_1 = QRadioButton(self.grid_defaults[0])
        self.grid_size_default_2 = QRadioButton(self.grid_defaults[1])
        self.grid_size_default_3 = QRadioButton(self.grid_defaults[2])
        self.grid_size_default_3.setChecked(True)
        self.none_selected = QRadioButton("hidden")

        # set to no focus to disable the arrow keys moving through the tabs (so they can be used for the target movement)
        self.grid_size_default_1.setFocusPolicy(Qt.NoFocus)
        self.grid_size_default_2.setFocusPolicy(Qt.NoFocus)
        self.grid_size_default_3.setFocusPolicy(Qt.NoFocus)

        # Add buttons to the group to make them exclusive
        grid_button_group = QButtonGroup()
        grid_button_group.setExclusive(True)
        grid_button_group.addButton(self.grid_size_default_1)
        grid_button_group.addButton(self.grid_size_default_2)
        grid_button_group.addButton(self.grid_size_default_3)
        grid_button_group.addButton(self.none_selected)

        # Connect the buttons to the slots
        self.grid_size_default_1.clicked.connect(self.radioButtonGridSizeChange)
        self.grid_size_default_2.clicked.connect(self.radioButtonGridSizeChange)
        self.grid_size_default_3.clicked.connect(self.radioButtonGridSizeChange)
        self.none_selected.toggled.connect(self.radioButtonGridSizeChange)

        # Add the buttons to the layout
        grid_setup_layout.addWidget(quick_size_label)
        quick_size_layout.addWidget(self.grid_size_default_1)
        quick_size_layout.addWidget(self.grid_size_default_2)
        quick_size_layout.addWidget(self.grid_size_default_3)

        # Add the quick sizes to the grid set up layout
        grid_setup_layout.addLayout(quick_size_layout)

        # Set up the other sizes in the dropdown menu
        self.dim_select = QComboBox()

        # set to no focus to disable the arrow keys moving through the tabs (so they can be used for the target movement)
        self.dim_select.setFocusPolicy(Qt.NoFocus)

        # Add all the different possible dims for grid
        for x in range(10, 61, 5):
            self.dim_select.addItem(str(x) + "x" + str(x))

        # Connect the dropdown menus (grid dims) to their slots
        self.dim_select.currentTextChanged.connect(self.dropDownGridSizeChange)

        # Default from config file - comment
        # self.var.dim = self.var.config.get("test", "grid_size_start_default")
        self.var.dim = self.grid_defaults[2]
        self.dim_select.setCurrentIndex(self.dim_select.findText(self.var.dim))

        # Add the dropdown and its label to the grid set up layout
        grid_setup_layout.addWidget(dim_menu_label)
        grid_setup_layout.addWidget(self.dim_select)

        # Selected Reference point/ reset button
        self.ref_pt_button = QPushButton()
        self.ref_pt_button.setText("Set Reference Point")
        self.ref_pt_label = QLabel("")

        # set to no focus to disable the arrow keys moving through the tabs (so they can be used for the target movement)
        self.ref_pt_button.setFocusPolicy(Qt.NoFocus)

        # Connect the reference point button to its slot
        self.ref_pt_button.clicked.connect(self.referencePointBttnClicked)

        # Add the Reference button and label to the main layout
        layout.addWidget(QLabel(""))
        grid_setup_layout.addWidget(self.ref_pt_button)
        grid_setup_layout.addWidget(self.ref_pt_label)

        # # Swap the view of T/N labels
        # view_layout = QHBoxLayout()
        # self.anatomical_view = QRadioButton("Anatomical View")
        # self.anatomical_view.setChecked(True)
        # self.subject_view = QRadioButton("Subject View")
        #
        # # Connect the View Radio buttons to the slot
        # self.anatomical_view.toggled.connect(self.viewChange)
        # self.subject_view.toggled.connect(self.viewChange)
        #
        # # Add view buttons to their layout and the main
        # view_layout.addWidget(self.anatomical_view)
        # view_layout.addWidget(self.subject_view)
        #
        # # Add view buttons to the grid set up layout
        # grid_setup_layout.addLayout(view_layout)

        # Add the grid set up layout to the grid Group layout and then add the group to the main layout as another row
        grid_config_group.setLayout(grid_setup_layout)
        layout.addRow(grid_config_group)

        # Image Calibration Group
        image_config_group = QGroupBox("Image Calibration")
        image_cal_layout = QVBoxLayout()

        # Attributes needed to display an image
        self.image_label = QLabel("")

        # Generate buttons needed for image calibration control
        self.load_bg_image_button = QPushButton()
        self.load_bg_image_button.setText("Load Background Image")  # Open file explore and select image
        self.image_cal_button = QPushButton()
        self.image_cal_button.setText("Start Image Calibration")
        center_fovea_button = QPushButton()
        center_fovea_button.setText("Center Fovea")

        self.load_bg_image_button.setFocusPolicy(Qt.NoFocus)
        self.image_cal_button.setFocusPolicy(Qt.NoFocus)
        center_fovea_button.setFocusPolicy(Qt.NoFocus)

        # Add the image calibration button to its slot when pressed
        self.image_cal_button.clicked.connect(self.onPressCal)
        self.load_bg_image_button.clicked.connect(self.onPressLoad)

        # Add all the widgets to the main layout and set priority
        image_cal_layout.addWidget(self.load_bg_image_button)
        image_cal_layout.addWidget(self.image_label)
        image_cal_layout.addWidget(self.image_cal_button)
        image_cal_layout.addWidget(center_fovea_button)

        # Add the protocol layout to the group layout and then add the group to the main layout as another row
        image_config_group.setLayout(image_cal_layout)
        layout.addRow(image_config_group)

        # Target set up group and its layout
        target_config_group = QGroupBox("Target Set Up")
        target_cal_layout = QVBoxLayout()

        # Color wheel for selecting the color of the target
        color_button = QPushButton("Select Color")
        target_cal_layout.addWidget(color_button)
        color_display = QHBoxLayout()
        self.color_name_label = QLabel("")
        self.color_display_label = QLabel()
        color_button.clicked.connect(self.onPressColor)

        color_button.setFocusPolicy(Qt.NoFocus)

        # Add all the Color related widgets to their layout
        color_display.addWidget(self.color_name_label)
        color_display.addWidget(self.color_display_label)
        target_cal_layout.addLayout(color_display)

        # Generate the scroll bar for the size of the fixation target
        self.size_bar = QSlider(Qt.Horizontal)
        # set to no focus to disable the arrow keys from moving the size
        self.size_bar.setFocusPolicy(Qt.NoFocus)
        self.label_size = QLabel()
        self.size_bar.setMinimum(1)
        self.size_bar.setMaximum(20)
        self.size_bar.setValue(self.var.size)
        self.size_bar.setTickPosition(QSlider.TicksBelow)
        self.size_bar.setTickInterval(1)
        self.label_size.setText("Target Size: " + str(self.var.size))
        self.size_bar.valueChanged.connect(self.sizeChange)

        # Add scroll bar and label to the main widget
        target_cal_layout.addWidget(self.label_size)
        target_cal_layout.addWidget(self.size_bar)

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
        buttonSize = 40
        self.cross.setFixedSize(QSize(buttonSize, buttonSize))
        self.s_cross.setFixedSize(QSize(buttonSize, buttonSize))
        self.m_cross.setFixedSize(QSize(buttonSize, buttonSize))
        self.square_out.setFixedSize(QSize(buttonSize, buttonSize))
        self.square.setFixedSize(QSize(buttonSize, buttonSize))
        self.circle.setFixedSize(QSize(buttonSize, buttonSize))
        self.twinkle.setFixedSize(QSize(buttonSize, buttonSize))

        self.cross.setFocusPolicy(Qt.NoFocus)
        self.s_cross.setFocusPolicy(Qt.NoFocus)
        self.m_cross.setFocusPolicy(Qt.NoFocus)
        self.square.setFocusPolicy(Qt.NoFocus)
        self.circle.setFocusPolicy(Qt.NoFocus)
        self.twinkle.setFocusPolicy(Qt.NoFocus)

        # Call the functions to draw the different targets
        self.drawTargets()

        # Adding the radio buttons to the shape layouts
        fix_shape_main = QVBoxLayout()
        fix_shape1 = QHBoxLayout()
        fix_shape1.addWidget(self.cross)
        fix_shape1.addWidget(self.s_cross)
        fix_shape1.addWidget(self.m_cross)
        fix_shape1.addWidget(self.square)
        fix_shape1.addWidget(self.circle)
        fix_shape1.addWidget(self.twinkle)
        fix_shape_main.addLayout(fix_shape1)

        # What will happen when a specific radio button is called
        self.cross.clicked.connect(self.onClick)
        self.s_cross.clicked.connect(self.onClick)
        self.m_cross.clicked.connect(self.onClick)
        self.square.clicked.connect(self.onClick)
        self.circle.clicked.connect(self.onClick)
        self.twinkle.clicked.connect(self.onClick)

        # Add the components to the target cl layout
        target_cal_layout.addWidget(QLabel(""))
        target_cal_layout.addLayout(fix_shape_main)
        target_cal_layout.addWidget(self.test_label)

        # Add the fixation target stuff to the main layout and then add the group to the main layout as another row
        target_config_group.setLayout(target_cal_layout)
        layout.addRow(target_config_group)

        # Set the main layout for the tab
        self.tab1.setLayout(layout)

    # will need to add slot to get checkbox to work also need to set default to be checked (grid visibility)
    def imagingTab(self):
        """
        Function for the UI properties and functionality for the imaging tab
        Components:
            - Protocol
                * Advance protocol Button
            - Target Control
                * user entered X/Y locations
                * Target animation (yes/no) and speed of animation
                * Target visible (yes/no)
                * Quick locations
            - Grid Visibility
                * Grid visible (yes/no - default yes)
            - Savior Control
                * Number of frames
                * Current FOV
        :return:
        """
        # Main tab layout
        layout = QFormLayout()

        # Info group
        info_group = QGroupBox("Info")
        info_layout = QVBoxLayout()

        # add the information we want
        info_layout.addWidget(QLabel("Subject ID: " + self.var.sub_id))
        info_layout.addWidget(QLabel("Eye: " + self.var.eye))
        info_layout.addWidget(QLabel("FOV: " + self.var.current_fov))

        # Add the info layout to the group and then the group to the main layout as another row
        info_group.setLayout(info_layout)
        layout.addRow(info_group)


        # Protocol Advance group
        protocol_group = QGroupBox("Protocol")
        protocol_adv_layout = QVBoxLayout()

        # Make and set up the advance protocol push button
        self.save_p_button = QPushButton()
        self.save_p_button.setText("Advance")
        self.save_p_label = QLabel()

        # Add the protocol buttons to its slots
        self.save_p_button.clicked.connect(self.onPressAdvanceP)

        # Add all the widgets to the group's layout
        protocol_adv_layout.addWidget(self.save_p_button)
        protocol_adv_layout.addWidget(self.save_p_label)

        # Add the protocol layout to the group and then the group to the main layout as another row
        protocol_group.setLayout(protocol_adv_layout)
        layout.addRow(protocol_group)

        # Group for the target location and movement
        target_control_group = QGroupBox("Target Control")
        target_control_layout = QVBoxLayout()

        # User input target control
        loc_layout = QHBoxLayout()
        self.horz = QLineEdit()
        self.vert = QLineEdit()
        self.horz.installEventFilter(self)
        self.vert.installEventFilter(self)

        self.horz.textChanged.connect(self.textChanged)
        self.vert.textChanged.connect(self.textChanged)

        # Add the Components to the location control layout
        loc_layout.addWidget(QLabel("X"))
        loc_layout.addWidget(self.horz)
        loc_layout.addWidget(QLabel("Y"))
        loc_layout.addWidget(self.vert)

        # Add the location layout to the target control layout
        target_control_layout.addLayout(loc_layout)

        # Animation of target
        animate_layout = QHBoxLayout()
        self.animation = QCheckBox(
            "Target Animation")  # will need to figure out slot for this to have it work correctly
        self.animation_speed = QLineEdit()
        self.animation.setFocusPolicy(Qt.NoFocus)
        self.animation_speed.installEventFilter(self)
        # self.animation_speed.setFocusPolicy(Qt.NoFocus)

        # Slot for the checkbox asking if target animation is on
        self.animation.stateChanged.connect(self.checkBoxResponse)

        # Add the components to the animate layout
        animate_layout.addWidget(self.animation)
        animate_layout.addWidget(QLabel("Deg/s:"))
        animate_layout.addWidget(self.animation_speed)

        # Add the animate layout to the target control layout
        target_control_layout.addLayout(animate_layout)

        # Target display on/off layout and checkboxes
        target_display_bttns = QHBoxLayout()
        self.target_vis_bttn = QCheckBox("Target Visible")
        self.target_vis_bttn.setChecked(self.var.target_vis)
        self.target_vis_bttn.setFocusPolicy(Qt.NoFocus)

        # Connect the checkbox to their slot
        self.target_vis_bttn.stateChanged.connect(self.checkBoxResponse)

        # Add the checkboxes to the target button layout
        target_display_bttns.addWidget(self.target_vis_bttn)

        # Add the target button layout to the target control layout
        target_control_layout.addLayout(target_display_bttns)

        # Add label for quick location to the target control layout
        target_control_layout.addWidget(QLabel("Quick Locations:"))

        # Quick Location Push buttons generated along with gridlayout for the buttons
        quick_bttn_layout = QGridLayout()

        # Push Buttons to be used for Quick Locations
        self.TRC = QPushButton("TRC")
        self.MTE = QPushButton("MTE")
        self.TLC = QPushButton("TLC")
        self.MLE = QPushButton("MLE")
        self.BLC = QPushButton("BLC")
        self.MBE = QPushButton("MBE")
        self.BRC = QPushButton("BRC")
        self.MRE = QPushButton("MRE")
        self.CTR = QPushButton("CTR")

        self.TRC.setFocusPolicy(Qt.NoFocus)
        self.MTE.setFocusPolicy(Qt.NoFocus)
        self.TLC.setFocusPolicy(Qt.NoFocus)
        self.MLE.setFocusPolicy(Qt.NoFocus)
        self.BLC.setFocusPolicy(Qt.NoFocus)
        self.MBE.setFocusPolicy(Qt.NoFocus)
        self.BRC.setFocusPolicy(Qt.NoFocus)
        self.MRE.setFocusPolicy(Qt.NoFocus)
        self.CTR.setFocusPolicy(Qt.NoFocus)


        # Change the shape of the buttons to be squares
        size = 30
        self.TRC.setFixedSize(QSize(size, size))
        self.MTE.setFixedSize(QSize(size, size))
        self.TLC.setFixedSize(QSize(size, size))
        self.MLE.setFixedSize(QSize(size, size))
        self.BLC.setFixedSize(QSize(size, size))
        self.MBE.setFixedSize(QSize(size, size))
        self.BRC.setFixedSize(QSize(size, size))
        self.MRE.setFixedSize(QSize(size, size))
        self.CTR.setFixedSize(QSize(size, size))

        # Set these quick location buttons to their needed slot
        self.TRC.clicked.connect(self.onPressQuickLocs)
        self.MTE.clicked.connect(self.onPressQuickLocs)
        self.TLC.clicked.connect(self.onPressQuickLocs)
        self.MLE.clicked.connect(self.onPressQuickLocs)
        self.CTR.clicked.connect(self.onPressQuickLocs)
        self.MRE.clicked.connect(self.onPressQuickLocs)
        self.BLC.clicked.connect(self.onPressQuickLocs)
        self.MBE.clicked.connect(self.onPressQuickLocs)
        self.BRC.clicked.connect(self.onPressQuickLocs)

        # Add all the quick loc buttons to their grid layout
        quick_bttn_layout.addWidget(self.TRC, 0, 2)
        quick_bttn_layout.addWidget(self.MTE, 0, 1)
        quick_bttn_layout.addWidget(self.TLC, 0, 0)
        quick_bttn_layout.addWidget(self.MLE, 1, 0)
        quick_bttn_layout.addWidget(self.BLC, 2, 0)
        quick_bttn_layout.addWidget(self.MBE, 2, 1)
        quick_bttn_layout.addWidget(self.BRC, 2, 2)
        quick_bttn_layout.addWidget(self.MRE, 1, 2)
        quick_bttn_layout.addWidget(self.CTR, 1, 1)

        # Add the quick buttons to the main target control layout
        target_control_layout.addLayout(quick_bttn_layout)

        # Add all the target control elements to the group layout and then add it to the main layout as another row
        target_control_group.setLayout(target_control_layout)
        layout.addRow(target_control_group)

        # Group for the Grid visibility
        grid_vis_group = QGroupBox("Grid Visibility")
        grid_vis_layout = QHBoxLayout()

        # Make the grid visible checkbox and set default to be checked
        self.grid_vis = QCheckBox("Grid Visible")
        self.grid_vis.setChecked(self.var.grid_vis)
        self.grid_vis.setFocusPolicy(Qt.NoFocus)

        # Connect the slot of the checkbox for grid visible
        self.grid_vis.stateChanged.connect(self.checkBoxResponse)
        grid_vis_layout.addWidget(self.grid_vis)

        # Add the grid visible button and group to the main layout
        grid_vis_group.setLayout(grid_vis_layout)
        layout.addRow(grid_vis_group)

        # Group for Savior Controls
        savior_group = QGroupBox("Savior Control")
        savior_layout = QFormLayout()

        # get the FOVs from the config file to be added to the dropdown menu
        self.FOV_menu = QComboBox()
        self.var.savior_FOVs = self.var.config.get("test", "savior_FOVs").split("/")

        # adds all the FOVs in the list
        for x in self.var.savior_FOVs:
            self.FOV_menu.addItem(x)

        # sets the selection to the first one
        self.FOV_menu.setCurrentIndex(0)

        # Add the components to the savior layout
        self.n_frames = QLineEdit()
        savior_layout.addRow("Number of Frames:", self.n_frames)
        savior_layout.addRow("Current FOV:", self.FOV_menu)
        self.FOV_menu.setFocusPolicy(Qt.NoFocus)
        self.n_frames.installEventFilter(self)

        # Add the savior layout to the savior group and then add the group to the main layout as another row
        savior_group.setLayout(savior_layout)
        layout.addRow(savior_group)

        # Sets the main layout of the tab
        self.tab2.setLayout(layout)

    # Currently Complete with all components
    def stimControlTab(self):
        """
        Function for the UI properties and functionality of the Stimulus control tab
        """
        # Sets up the main layout of the tab
        layout = QFormLayout()

        # Set up the group and its layout for stimulus control
        stim_group = QGroupBox("Stimulus Control")
        stim_layout = QFormLayout()

        # Add the components to the group layout
        stim_layout.addRow("Port Number:", QLineEdit())
        stim_layout.addRow(QLabel(""))
        stim_layout.addRow(QLabel("Stimulus Parameters:"))
        stim_layout.addRow("Frequency: ", QLineEdit())
        stim_layout.addRow("Duration", QLineEdit())
        stim_layout.addRow("Start Time", QLineEdit())
        stim_layout.addRow("Frames After", QLineEdit())

        # Add the stimulus layout to the group and then add the group to the main layout as another row
        stim_group.setLayout(stim_layout)
        layout.addRow(stim_group)

        # Sets the tab's layout to the main layout
        self.tab3.setLayout(layout)

    # Currently complete with all needed components
    def sessionReview(self):
        """
        Function for the UI properties and functionality for the session review tab
        :return:
        """
        # Set up the main layout for the tab
        layout = QFormLayout()

        # Protocol Advance group and its layout
        save_grid_group = QGroupBox("Save Grid Display")
        save_grid_layout = QVBoxLayout()

        # Save current grid push button
        self.grid_display_save = QPushButton()
        self.grid_display_save.setText("Save Current Grid Display")

        # Connect to the slot and add to main layout
        self.grid_display_save.clicked.connect(self.saveGrid)
        save_grid_layout.addWidget(self.grid_display_save)

        # Add the save grid layout to its group and then add the group to the main layout as another row
        save_grid_group.setLayout(save_grid_layout)
        layout.addRow(save_grid_group)

        # Add the Nuclear info to the final review tab
        info_group = QGroupBox("Session Information")

        info_layout = QFormLayout()
        info_layout.addRow("Eye:", QLabel(self.var.eye))
        info_layout.addRow("Subject ID:", QLabel(self.var.sub_id))
        info_layout.addRow("Device:", QLabel(self.var.device))
        info_layout.addRow(QLabel(""))
        info_layout.addRow("FOV:", QLabel(self.var.current_fov))
        info_layout.addRow(QLabel(""))
        info_layout.addRow(QLabel("Document Save Location:"))
        info_layout.addRow(QLabel(self.var.save_loc))

        # Add the info layout to its group and then add the group to the main layout as another row
        info_group.setLayout(info_layout)
        layout.addRow(info_group)

        # Set the tab's layout to the main one
        self.tab4.setLayout(layout)

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
        self.drawSquare()
        self.drawSquareOutline()
        self.drawCircle()
        self.drawTwinkle()
        self.drawMaltcross()

    def drawCross(self):
        canvas = QtGui.QPixmap(QSize(100, 100))
        canvas.fill(Qt.black)
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen(self.var.custom_color, 15)
        painter.setPen(pen)
        painter.drawLine(10, 50, 90, 50)
        painter.drawLine(50, 10, 50, 90)
        painter.end()
        self.cross.setIcon(canvas)
        self.cross.setIconSize(QSize(32, 32))
        self.cross.setStyleSheet("text-align: left;")

    def drawSmallCross(self):
        canvas = QtGui.QPixmap(QSize(100, 100))
        canvas.fill(Qt.black)
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen(self.var.custom_color, 15)
        painter.setPen(pen)
        painter.drawLine(35, 50, 65, 50)
        painter.drawLine(50, 35, 50, 65)
        painter.end()
        self.s_cross.setIcon(canvas)
        self.s_cross.setIconSize(QSize(32, 32))
        self.s_cross.setStyleSheet("text-align: left;")

    def drawSquare(self):
        canvas = QtGui.QPixmap(QSize(100, 100))
        canvas.fill(Qt.black)
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen(self.var.custom_color, 15)
        painter.setPen(pen)
        painter.setBrush(self.var.custom_color)
        painter.drawRect(15, 15, 70, 70)
        painter.end()
        self.square.setIcon(canvas)
        self.square.setIconSize(QSize(32, 32))
        self.square.setStyleSheet("text-align: left;")

    def drawSquareOutline(self):
        canvas = QtGui.QPixmap(QSize(100, 100))
        canvas.fill(Qt.black)
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen(self.var.custom_color, 15)
        painter.setPen(pen)
        painter.drawLine(20, 20, 20, 80)
        painter.drawLine(20, 20, 80, 20)
        painter.drawLine(80, 20, 80, 80)
        painter.drawLine(20, 80, 80, 80)
        painter.end()
        self.square_out.setIcon(canvas)
        self.square_out.setIconSize(QSize(32, 32))
        self.square_out.setStyleSheet("text-align: left;")

    def drawCircle(self):
        canvas = QtGui.QPixmap(QSize(100, 100))
        canvas.fill(Qt.black)
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen(self.var.custom_color, 15)
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(self.var.custom_color))
        center = QPointF(50, 50)
        painter.drawEllipse(center, 35, 35)
        painter.end()
        self.circle.setIcon(canvas)
        self.circle.setIconSize(QSize(32, 32))
        self.circle.setStyleSheet("text-align: left;")

    def drawTwinkle(self):
        canvas = QtGui.QPixmap(QSize(100, 100))
        canvas.fill(Qt.black)
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen(self.var.custom_color, 10)
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
        self.twinkle.setIconSize(QSize(32, 32))
        self.twinkle.setStyleSheet("text-align: left;")

    def drawMaltcross(self):
        canvas = QtGui.QPixmap(QSize(100, 100))
        canvas.fill(Qt.black)
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen(self.var.custom_color, 10)
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
        self.m_cross.setIconSize(QSize(32, 32))
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
                self.var.shape = txt
                self.test_label.setText("You pressed the button called: " + txt)
            case "Small Crosshair":
                # Will be changed to what each shape will look like in the future
                self.var.shape = txt
                self.test_label.setText("You pressed the button called: " + txt)
            case "Maltese Cross":
                # Will be changed to what each shape will look like in the future
                self.var.shape = txt
                self.test_label.setText("You pressed the button called: " + txt)
            case "Square Outline":
                # Will be changed to what each shape will look like in the future
                self.var.shape = txt
                self.test_label.setText("You pressed the button called: " + txt)
            case "Square":
                # Will be changed to what each shape will look like in the future
                self.var.shape = txt
                self.test_label.setText("You pressed the button called: " + txt)
            case "Circle":
                # Will be changed to what each shape will look like in the future
                self.var.shape = txt
                self.test_label.setText("You pressed the button called: " + txt)
            case "Twinkle":
                # Will be changed to what each shape will look like in the future
                self.var.shape = txt
                self.test_label.setText("You pressed the button called: " + txt)

    def sizeChange(self):
        """
        Slot for displaying the size of the fixation target as it moves
        """
        txt = "Target Size: " + str(self.size_bar.value())
        self.label_size.setText(txt)
        self.var.size = self.size_bar.value()

    def onPressColor(self):
        """
        Slot used to select the color of the fixation target
        """
        color = QColorDialog.getColor()  # Might want to make a class variable to change the color of the fixation target to the one selected
        self.var.custom_color = color
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

    # def onPressLoadP(self):
    #     button = self.sender()
    #     protocol_path = filedialog.askopenfilenames(title='Select the protocol to load', filetypes=[
    #         ("protocol", ".csv")])
    #     print(protocol_path)
    #     self.load_p_label.setText(str(protocol_path))

    def onPressAdvanceP(self):
        button = self.sender()
        txt = self.save_p_label.text()
        match txt:
            case "Advance in Protocol":
                self.save_p_label.setText("")
            case _:
                self.save_p_label.setText("Advance in Protocol")

    def onPressQuickLocs(self):
        button = self.sender()
        txt = str(button.text())
        tmp = self.var.current_fov.split(" ")
        h_fov = float(tmp[0])
        v_fov = float(tmp[2])
        # need to make sure these end up being in the correct locations
        match txt:
            case "TLC":
                self.var.x_val = 0 - (h_fov / 4)
                self.var.y_val = 0 + (v_fov / 4)
                self.var.center_x = self.var.center_x_og - ((h_fov/4) * self.var.screen_ppd)
                self.var.center_y = self.var.center_y_og - ((v_fov/4) * self.var.screen_ppd)
                self.var.center_x_grid = self.var.center_x_og_grid - ((h_fov / 4) * self.var.grid_mult)
                self.var.center_y_grid = self.var.center_y_og_grid - ((v_fov / 4) * self.var.grid_mult)
            case "MTE":
                self.var.x_val = 0
                self.var.y_val = 0 + (v_fov / 4)
                self.var.center_x = self.var.center_x_og
                self.var.center_y = self.var.center_y_og - ((v_fov/4) * self.var.screen_ppd)
                self.var.center_x_grid = self.var.center_x_og_grid
                self.var.center_y_grid = self.var.center_y_og_grid - ((v_fov / 4) * self.var.grid_mult)
            case "TRC":
                self.var.x_val = 0 + (h_fov / 4)
                self.var.y_val = 0 + (v_fov / 4)
                self.var.center_x = self.var.center_x_og + ((h_fov/4) * self.var.screen_ppd)
                self.var.center_y = self.var.center_y_og - ((v_fov/4) * self.var.screen_ppd)
                self.var.center_x_grid = self.var.center_x_og_grid + ((h_fov / 4) * self.var.grid_mult)
                self.var.center_y_grid = self.var.center_y_og_grid - ((v_fov / 4) * self.var.grid_mult)
            case "MLE":
                self.var.x_val = 0 - (h_fov / 4)
                self.var.y_val = 0
                self.var.center_x = self.var.center_x_og - ((h_fov/4) * self.var.screen_ppd)
                self.var.center_y = self.var.center_y_og
                self.var.center_x_grid = self.var.center_x_og_grid - ((h_fov / 4) * self.var.grid_mult)
                self.var.center_y_grid = self.var.center_y_og_grid
            case "CTR":
                self.var.x_val = 0
                self.var.y_val = 0
                self.var.center_x = self.var.center_x_og
                self.var.center_y = self.var.center_y_og
                self.var.center_x_grid = self.var.center_x_og_grid
                self.var.center_y_grid = self.var.center_y_og_grid
            case "MRE":
                self.var.x_val = 0 + (h_fov / 4)
                self.var.y_val = 0
                self.var.center_x = self.var.center_x_og + ((h_fov/4) * self.var.screen_ppd)
                self.var.center_y = self.var.center_y_og
                self.var.center_x_grid = self.var.center_x_og_grid + ((h_fov / 4) * self.var.grid_mult)
                self.var.center_y_grid = self.var.center_y_og_grid
            case "BLC":
                self.var.x_val = 0 - (h_fov / 4)
                self.var.y_val = 0 - (v_fov / 4)
                self.var.center_x = self.var.center_x_og - ((h_fov/4) * self.var.screen_ppd)
                self.var.center_y = self.var.center_y_og + ((v_fov/4) * self.var.screen_ppd)
                self.var.center_x_grid = self.var.center_x_og_grid - ((h_fov / 4) * self.var.grid_mult)
                self.var.center_y_grid = self.var.center_y_og_grid + ((v_fov / 4) * self.var.grid_mult)
            case "MBE":
                self.var.x_val = 0
                self.var.y_val = 0 - (v_fov / 4)
                self.var.center_x = self.var.center_x_og
                self.var.center_y = self.var.center_y_og + ((v_fov/4) * self.var.screen_ppd)
                self.var.center_x_grid = self.var.center_x_og_grid
                self.var.center_y_grid = self.var.center_y_og_grid + ((v_fov / 4) * self.var.grid_mult)
            case "BRC":
                self.var.x_val = 0 + (h_fov / 4)
                self.var.y_val = 0 - (v_fov / 4)
                self.var.center_x = self.var.center_x_og + ((h_fov/4) * self.var.screen_ppd)
                self.var.center_y = self.var.center_y_og + ((v_fov/4) * self.var.screen_ppd)
                self.var.center_x_grid = self.var.center_x_og_grid + ((h_fov / 4) * self.var.grid_mult)
                self.var.center_y_grid = self.var.center_y_og_grid + ((v_fov / 4) * self.var.grid_mult)
            case _:
                print("Something went wrong!")

        # call to update the coordinates in the horz and vert text boxes
        self.updateCoordText()

    """
    slots for the Grid Configuration Tab
    """
    def radioButtonGridSizeChange(self):
        """
        Slot for the grid default quick sizes to be changed
        :return: None
        """
        button = self.sender()
        txt = button.text()
        if button.isChecked():
            print("Pressed the button called: " + txt)
            v1 = str(self.grid_defaults[0])
            v2 = str(self.grid_defaults[1])
            v3 = str(self.grid_defaults[2])
            v4 = str(self.none_selected.text())
            if txt == v1:
                self.var.dim = self.grid_defaults[0]
                self.dim_select.setCurrentIndex(self.dim_select.findText(self.var.dim))
            elif txt == v2:
                self.var.dim = self.grid_defaults[1]
                self.dim_select.setCurrentIndex(self.dim_select.findText(self.var.dim))
            elif txt == v3:
                self.var.dim = self.grid_defaults[2]
                self.dim_select.setCurrentIndex(self.dim_select.findText(self.var.dim))
            elif txt == v4:
                print("hidden button")
            else:
                print("Something went wrong!")

    def dropDownGridSizeChange(self):
        """
        Slot for the drop-down menu for the grid sizes allowed
        :return: None
        """
        self.var.dim = self.dim_select.currentText()
        print(" ")
        txt = self.var.dim
        print("Selected dim: " + txt)
        v1 = str(self.grid_defaults[0])
        print(v1 + "b")
        v2 = str(self.grid_defaults[1])
        print(v2 + "b")
        v3 = str(self.grid_defaults[2])
        print(v3 + "b")
        if txt == v1:
            self.dim_select.setCurrentIndex(self.dim_select.findText(self.var.dim))
            self.grid_size_default_1.setChecked(True)
        elif txt == v2:
            self.grid_size_default_2.setChecked(True)
            self.dim_select.setCurrentIndex(self.dim_select.findText(self.var.dim))
        elif txt == v3:
            self.grid_size_default_3.setChecked(True)
            self.dim_select.setCurrentIndex(self.dim_select.findText(self.var.dim))
        else:
            print("Non Default selected!")
            self.none_selected.setChecked(True)

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
            if txt == "Subject View":
                self.var.label_or = not self.var.label_or
            if txt == "Anatomical View":
                self.var.label_or = not self.var.label_or
            print(self.var.label_or)

    def saveGrid(self):
        """
        Slot for the save grid display button
        :return:
        """
        button = self.sender()
        print(button.text())

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
                    self.var.target_vis = False
                    print(self.var.target_vis)
                else:
                    self.var.target_vis = True
            case "Grid Visible":
                if button.checkState() == PySide6.QtCore.Qt.CheckState.Unchecked:
                    self.var.grid_vis = False
                    print(self.var.grid_vis)
                else:
                    self.var.grid_vis = True
            case _:
                print("Something went wrong!")
        print(txt)


    def updateCoordText(self):
        """
        Update the coordinate text in the horz and vert text boxes (called when the location changed)
        Rounds value to 2 decimal places
        :return:
        """
        self.horz.setText(str(round(self.var.x_val, 2)))
        self.vert.setText(str(round(self.var.y_val, 2)))

    def textChanged(self):
        """
        When the text is changed in a text box check what text box sent the signal and then extract the text
        If it is from the horz or vert (x and y coordinates) then update the x and y values
        :return:
        """
        txt_box = self.sender()
        txt = txt_box.text()
        if txt_box == self.horz:
            self.var.x_val = float(txt)
        if txt_box == self.vert:
            self.var.y_val = float(txt)


    def eventFilter(self, source, event, keyboard=None):
        """
        clears the focus on the text boxes when arrow keys or enter is pressed
        :param source: the source of the event
        :param event: the event
        :return:
        """
        if source == self.horz and event.type() == QEvent.Type.KeyPress:
            if event.key() == (QtCore.Qt.Key_Up):
                self.horz.clearFocus()
            elif event.key() == (QtCore.Qt.Key_Down):
                self.horz.clearFocus()
            elif event.key() == (QtCore.Qt.Key_Left):
                self.horz.clearFocus()
            elif event.key() == (QtCore.Qt.Key_Right):
                self.horz.clearFocus()
            elif event.key() == (QtCore.Qt.Key_Enter):
                self.horz.clearFocus()
        if source == self.vert and event.type() == QEvent.Type.KeyPress:
            if event.key() == (QtCore.Qt.Key_Up):
                self.vert.clearFocus()
            elif event.key() == (QtCore.Qt.Key_Down):
                self.vert.clearFocus()
            elif event.key() == (QtCore.Qt.Key_Left):
                self.vert.clearFocus()
            elif event.key() == (QtCore.Qt.Key_Right):
                self.vert.clearFocus()
            elif event.key() == (QtCore.Qt.Key_Enter):
                self.vert.clearFocus()
        if source == self.animation_speed and event.type() == QEvent.Type.KeyPress:
            if event.key() == (QtCore.Qt.Key_Up):
                self.animation_speed.clearFocus()
            elif event.key() == (QtCore.Qt.Key_Down):
                self.animation_speed.clearFocus()
            elif event.key() == (QtCore.Qt.Key_Left):
                self.animation_speed.clearFocus()
            elif event.key() == (QtCore.Qt.Key_Right):
                self.animation_speed.clearFocus()
            elif event.key() == (QtCore.Qt.Key_Enter):
                self.animation_speed.clearFocus()
        if source == self.n_frames and event.type() == QEvent.Type.KeyPress:
            if event.key() == (QtCore.Qt.Key_Up):
                self.n_frames.clearFocus()
            elif event.key() == (QtCore.Qt.Key_Down):
                self.n_frames.clearFocus()
            elif event.key() == (QtCore.Qt.Key_Left):
                self.n_frames.clearFocus()
            elif event.key() == (QtCore.Qt.Key_Right):
                self.n_frames.clearFocus()
            elif event.key() == (QtCore.Qt.Key_Enter):
                self.n_frames.clearFocus()
        return super().eventFilter(source, event)



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Tabs()
    widget.resize(800, 800)
    widget.show()

    sys.exit(app.exec())
