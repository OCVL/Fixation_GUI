from tkinter import filedialog
import PySide6
from PySide6 import QtWidgets, QtGui, QtCore
import sys
from PySide6.QtGui import *
from PySide6.QtCore import Qt, QSize, QPointF, QEvent, QRegularExpression, Signal, Property, Slot
from PySide6.QtWidgets import *

from ocvl.fixation.targets import TargetFactory, MalteseCross, CrossHair, TargetTypes, Target


class ControlPanel(QTabWidget):
    """
    Main class for the control panel that contains various tabs, each with different functionality
    """
    targetChanged = Signal(Target)

    def __init__(self, config: dict, parent=None):
        super().__init__(parent)

        if config is None:
            self.config = dict()
        else:
            self.config = config

        self.part_config = self.config.get("participant_display", dict())

        # Target variables
        self.target_color = QColor(self.part_config.get("color", "orange"))
        self.target_shape = self.part_config.get("shape", TargetTypes.BULLSEYE)
        self.target_diameter = self.part_config.get("diameter", 1)
        self.target_thickness = self.part_config.get("thickness", 0.1)

        self.targetbuttons = {}

        # Generate the Tabs for the window to hold the settings
        self.setup_tab = QWidget()
        # self.imaging_tab = QWidget()
        # self.session_review = QWidget()

        # set to no focus to disable the arrow keys moving through the tabs (so they can be used for the target movement)
        self.setFocusPolicy(Qt.NoFocus)

        # Set the position of the tabs to be on the right
        self.setTabPosition(QTabWidget.East)
        self.setTabShape(QTabWidget.Triangular)

        # Add the tabs generated to the parent window
        self.addTab(self.setup_tab, "Setup")
        # self.addTab(self.imaging_tab, "Imaging")
        # self.addTab(self.session_review, "Session Review")

        # UI functions for the new tab layout
        self.guiSetUp()
        # self.imagingTab()
        # self.sessionReview()

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
        self.center_fovea_button = QPushButton()
        self.center_fovea_button.setText("Center Fovea")

        self.load_bg_image_button.setFocusPolicy(Qt.NoFocus)
        self.image_cal_button.setFocusPolicy(Qt.NoFocus)
        self.center_fovea_button.setFocusPolicy(Qt.NoFocus)

        # Add the image calibration button to its slot when pressed
        self.image_cal_button.clicked.connect(self.onPressCal)
        self.load_bg_image_button.clicked.connect(self.onPressLoad)

        # Add all the widgets to the main layout and set priority
        image_cal_layout.addWidget(self.load_bg_image_button)
        image_cal_layout.addWidget(self.image_label)
        image_cal_layout.addWidget(self.image_cal_button)
        image_cal_layout.addWidget(self.center_fovea_button)

        # Add the protocol layout to the group layout and then add the group to the main layout as another row
        image_config_group.setLayout(image_cal_layout)
        layout.addRow(image_config_group)

        # Target set up group and its layout
        target_config_group = QGroupBox("Target Properties")
        target_cal_layout = QVBoxLayout()

        # Generate the scroll bar for the size of the fixation target
        self.size_spinner = QDoubleSpinBox()
        # set to no focus to disable the arrow keys from moving the size
        self.size_spinner.setFocusPolicy(Qt.NoFocus)
        self.label_size = QLabel()
        self.size_spinner.setMinimum(1 / self.part_config.get("ppd", 10))
        self.size_spinner.setMaximum(5 * self.part_config.get("ppd", 10))
        self.size_spinner.setValue(self.part_config.get("diameter", 1))
        self.size_spinner.setSingleStep(1 / self.part_config.get("ppd", 10))

        self.label_size.setText(f"Diameter: {self.part_config.get("diameter", 1):.2f}{chr(0x00B0)}")
        self.size_spinner.valueChanged.connect(self.sizeChange)

        # Add scroll bar and label to the main widget
        target_cal_layout.addWidget(self.label_size)
        target_cal_layout.addWidget(self.size_spinner)

        # Color wheel for selecting the color of the target
        color_button = QPushButton("Select Color")
        target_cal_layout.addWidget(color_button)
        color_button.clicked.connect(self.onPressColor)

        color_button.setFocusPolicy(Qt.NoFocus)

        # Adding the buttons to the shape layouts
        fix_shape_main = QVBoxLayout()
        fix_shape1 = QHBoxLayout()
        self.target_buttongroup = QButtonGroup()

        # Push Buttons to be used for target shape
        for target in TargetTypes:
            self.targetbuttons[target] = QPushButton()
            self.targetbuttons[target].setObjectName(target)
            self.targetbuttons[target].setFixedSize(QSize(48, 48))
            self.targetbuttons[target].setFocusPolicy(Qt.NoFocus)
            self.targetbuttons[target].setCheckable(True)
            self.targetbuttons[target].clicked.connect(self.updateTargets)
            self.target_buttongroup.addButton(self.targetbuttons[target])

            if target == self.target_shape:
                self.targetbuttons[target].setChecked(True)

            fix_shape1.addWidget(self.targetbuttons[target])

        # Call the functions to draw the different targets
        self.updateTargets()

        fix_shape_main.addLayout(fix_shape1)

        # Add the components to the target cl layout
        target_cal_layout.addWidget(QLabel(""))
        target_cal_layout.addLayout(fix_shape_main)


        # Add the fixation target stuff to the main layout and then add the group to the main layout as another row
        target_config_group.setLayout(target_cal_layout)
        layout.addRow(target_config_group)

        # Set the main layout for the tab
        self.setup_tab.setLayout(layout)
    #
    # class MyObject(QObject):
    #     def __init__(self):
    #         super().__init__()
    #         self._name = "Default"
    #
    #     def get_name(self):
    #         return self._name
    #
    #     def set_name(self, value):
    #         self._name = value
    #
    #     # Define a bindable property
    #     name = Property(str, get_name, set_name, bindable=True)
    #
    # # Usage
    # obj = MyObject()
    # bindable_name = QBindable(obj, "name")
    # bindable_name.setBinding(lambda: "Bound Value")
    # print(obj.name)  # Output: Bound Value
    #
    # value = Property(str, fget=get_value, fset=set_value, notify=valueChanged)

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
        fov_layout = QGridLayout()

        # add the information we want
        info_layout.addWidget(QLabel("Subject ID: " + self.var.sub_id))
        info_layout.addWidget(QLabel("Eye: " + self.var.eye))
        fov_layout.addWidget(QLabel("FOV: "), 0, 0)
        self.info_fov = QLineEdit(self.var.current_fov)
        self.info_fov.setReadOnly(True)
        self.info_fov.setFrame(False)
        fov_layout.addWidget(self.info_fov, 0, 1)
        info_layout.addLayout(fov_layout)


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

        # added to ensure nothing other than a float number is able to be typed into the text boxes
        self.horz.setValidator(QDoubleValidator(-100.0, 100.0, 2, notation=QtGui.QDoubleValidator.StandardNotation))
        self.vert.setValidator(QDoubleValidator(-100.0, 100.0, 2, notation=QtGui.QDoubleValidator.StandardNotation))

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

        # Sets the main layout of the tab
        self.imaging_tab.setLayout(layout)


    # Currently complete with all needed components
    def sessionReview(self):
        """
        Function for the UI properties and functionality for the session review tab
        :return:
        """
        # Set up the main layout for the tab
        layout = QFormLayout()

        # # Protocol Advance group and its layout
        # save_grid_group = QGroupBox("Save Grid Display")
        # save_grid_layout = QVBoxLayout()
        #
        # # Save current grid push button
        # self.grid_display_save = QPushButton()
        # self.grid_display_save.setText("Save Current Grid Display")
        #
        # # Connect to the slot and add to main layout
        # self.grid_display_save.clicked.connect(self.saveGrid)
        # save_grid_layout.addWidget(self.grid_display_save)
        #
        # # Add the save grid layout to its group and then add the group to the main layout as another row
        # save_grid_group.setLayout(save_grid_layout)
        # layout.addRow(save_grid_group)

        # Add the Nuclear info to the final review tab
        info_group = QGroupBox("Session Information")

        info_layout = QFormLayout()
        info_layout.addRow("Eye:", QLabel(self.var.eye))
        info_layout.addRow("Subject ID:", QLabel(self.var.sub_id))
        info_layout.addRow("Device:", QLabel(self.var.device))
        info_layout.addRow(QLabel(""))
        self.fov_list = QListWidget()

        info_layout.addRow("FOV:", self.fov_list)
        info_layout.addRow(QLabel(""))
        info_layout.addRow(QLabel("Document Save Location:"))
        info_layout.addRow(QLabel(self.var.save_loc))

        # Add the info layout to its group and then add the group to the main layout as another row
        info_group.setLayout(info_layout)
        layout.addRow(info_group)

        # Set the tab's layout to the main one
        self.session_review.setLayout(layout)

    """
    Functions below are used in the UI for fixationTargetControlTab
    """
    def updateTargets(self):
        """
        Function that calls each function in charge of drawing on the fixation target to be selected
        """
        for target_type, button in self.targetbuttons.items():

            canvas = QtGui.QPixmap(QSize(64, 64))
            canvas.fill(Qt.black)
            painter = QPainter(canvas)
            painter.setTransform(QTransform.fromTranslate(32, 32))

            if button.isChecked():
                targ = TargetFactory.get_target(target_type, size=32, thickness=5, color=self.target_color)
                self.targetChanged.emit(TargetFactory.get_target(target_type, size=self.target_diameter, thickness=self.target_thickness, color=self.target_color))
            else:
                targ = TargetFactory.get_target(target_type, size=32, thickness=5, color=QColor("darkgray"))

            targ.paint(painter, QStyleOptionGraphicsItem(), None)
            painter.end()

            button.setIcon(canvas)
            button.setIconSize(QSize(32, 32))

    @Slot()
    def sizeChange(self, newval: float):
        """
        Slot for displaying the size of the fixation target as it moves
        """
        self.label_size.setText(f"Diameter: {newval:.2f}{chr(0x00B0)}")
        self.target_diameter = newval
        self.updateTargets()

    @Slot()
    def onPressColor(self):
        """
        Slot used to select the color of the fixation target
        """
        color = QColorDialog.getColor()  # Might want to make a class variable to change the color of the fixation target to the one selected
        self.target_color = color
        if color.isValid():
            self.updateTargets()

    """
    Slots that are used in the UI for imCalibrationControlTab
    """
    @Slot()
    def onPressCal(self):
        button = self.sender()
        txt = str(button.text())
        if txt == "Start Image Calibration":
            self.image_cal_button.setText("Select 1st Point on Image")
        elif txt == "Select 1st Point on Image":
            self.image_cal_button.setText("Select Corresponding Point (1st Point)")
        elif txt == "Select Corresponding Point (1st Point)":
            self.image_cal_button.setText("Select 2nd Point on Image")
        elif txt == "Select 2nd Point on Image":
            self.image_cal_button.setText("Select Corresponding Point (2nd Point)")
        elif txt == "Select Corresponding Point (2nd Point)":
            self.image_cal_button.setText("Select 3rd Point on Image")
        elif txt == "Select 3rd Point on Image":
            self.image_cal_button.setText("Select Corresponding Point (3rd Point)")
        elif txt == "Select Corresponding Point (3rd Point)":
            self.image_cal_button.setText("Start Calibration")
        elif txt == "Start Calibration":
            self.image_cal_button.setText("New Calibration")
        elif txt == "New Calibration":
            self.image_cal_button.setText("Start Image Calibration")


    def onPressLoad(self):
        button = self.sender()
        image_path = filedialog.askopenfilenames(title='Select the background image', filetypes=[
            ("image", ".jpeg"),
            ("image", ".png"),
            ("image", ".jpg"),
            ("image", ".tif")])
        print(image_path)
        self.image_path = image_path
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
        if txt =="Advance in Protocol":
            self.save_p_label.setText("")
        else:
            self.save_p_label.setText("Advance in Protocol")

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
            v1 = str(self.grid_defaults[0])
            v2 = str(self.grid_defaults[1])
            v3 = str(self.grid_defaults[2])
            v4 = str(self.none_selected.text())
            if txt == v1:
                self.var.dim = self.grid_defaults[0].split("x")
                # self.dim_select.setCurrentIndex(self.dim_select.findText(self.var.dim))
            elif txt == v2:
                self.var.dim = self.grid_defaults[1].split("x")
                # self.dim_select.setCurrentIndex(self.dim_select.findText(self.var.dim))
            elif txt == v3:
                self.var.dim = self.grid_defaults[2].split("x")
                # self.dim_select.setCurrentIndex(self.dim_select.findText(self.var.dim))
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
        if txt == "Set Reference Point":
            # Add a label to display what was selected as the current reference point
            self.ref_pt_label.setText("Reference Point (" + str(round(self.var.x_pos_deg, 2)) + "," + str(round(self.var.y_val, 2)) + ")")
            self.ref_pt_button.setText("Clear Reference Point")
            # set reference point to true and set the ref point values
            self.var.ref_point = True
            self.var.x_ref = self.var.x_pos_deg
            self.var.y_ref = self.var.y_val
        elif txt == "Clear Reference Point":
            self.ref_pt_button.setText("Set Reference Point")
            self.ref_pt_label.setText("")
            self.var.ref_point = False
        else:
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

    # def saveGrid(self):
    #     """
    #     Slot for the save grid display button
    #     :return:
    #     """
    #     button = self.sender()
    #     print(button.text())

    def checkBoxResponse(self):
        """
        Slot for if the fixation target is displayed to the subject
        :return:
        """
        button = self.sender()
        txt = button.text()
        if txt == "Target Animation":
            print(button.checkState())
        elif txt == "Target Visible":
            if button.checkState() == PySide6.QtCore.Qt.CheckState.Unchecked:
                self.var.target_vis = False
                print(self.var.target_vis)
            else:
                self.var.target_vis = True
        elif txt == "Grid Visible":
            if button.checkState() == PySide6.QtCore.Qt.CheckState.Unchecked:
                self.var.grid_vis = False
                print(self.var.grid_vis)
            else:
                self.var.grid_vis = True
        else:
            print("Something went wrong!")


    def updateCoordText(self):
        """
        Update the coordinate text in the horz and vert text boxes (called when the location changed)
        Rounds value to 2 decimal places
        :return:
        """
        self.horz.setText(str(round(self.var.x_pos_deg, 2)))
        self.vert.setText(str(round(self.var.y_val, 2)))

    def updateFOVText(self):
        """
        Update the FOV text in the info box (called when the FOV queue data comes in)
        :return:
        """
        self.info_fov.setText(self.var.current_fov)


    def textChanged(self):
        """
        When the text is changed in a text box check what text box sent the signal and then extract the text
        If it is from the horz or vert (x and y coordinates) then update the x and y values
        :return:
        """
        txt_box = self.sender()
        txt = txt_box.text()
        if txt_box == self.horz:
            self.var.x_pos_deg = float(txt)
        if txt_box == self.vert:
            self.var.y_val = float(txt)


    def eventFilter(self, source, event, keyboard=None):
        """
        clears the focus on the text boxes when arrow keys or enter is pressed
        :param source: the source of the event
        :param event: the event
        :return:
        """
        if event.type() == QEvent.Type.KeyPress and event.key() in (QtCore.Qt.Key_Up, QtCore.Qt.Key_Down, QtCore.Qt.Key_Left, QtCore.Qt.Key_Right):
            source.clearFocus()
        return super().eventFilter(source, event)



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = ControlPanel()
    widget.resize(800, 800)
    widget.show()

    sys.exit(app.exec())
