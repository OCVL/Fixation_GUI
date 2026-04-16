import configparser
import os
from queue import Queue
from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt, Signal, QObject

from ocvl.fixation.nuclear_target import TargetTypes
from ocvl.fixation.targets import CrossHair, Target


# using property class
class StatusVariables(QObject):
    shapeChanged = Signal(Target)
    xChanged = Signal(float)
    yChanged = Signal(float)

    def __init__(self, animation_speed=None, x_pos=0, y_pos=0, dim=None, \
                 custom_color=Qt.white, eye='OX', device=None, current_fov=(0.0, 0.0), target_shape=CrossHair(),
                 size=16, thickness=5, center_x=None, center_y=None, fixation_target_ppd=None):

        super().__init__()

        # Information (maybe) coming from elsewhere
        self.device = device
        self.eye = eye
        self.fov = current_fov

        # Target variables
        self.target_color = custom_color
        self.target_shape = target_shape
        self.target_size = size
        self.target_thickness = thickness

        # In degrees
        self.x_pos_deg = x_pos
        self.y_pos_deg = y_pos
        self.dim = dim
        # In pixels
        self.x_center_px = center_x
        self.y_center_px = center_y

        # Grid to Target conversion variables
        self.fixation_target_ppd = fixation_target_ppd
        self.grid_view_ppd =

        self.animation_speed = animation_speed

    # getter
    def get_stimulus_imaging(self):
        return self._stimulus_imaging

    # setter
    def set_stimulus_imaging(self, value):
        self._stimulus_imaging = value

    # getter
    def get_animation_speed_val(self):
        return self._animation_speed_val

    # setter
    def set_animation_speed_val(self, value):
        self._animation_speed_val = value

    # getter
    def get_x_val(self):
        return self._x_val

    # setter
    def set_x_val(self, value):
        self._x_val = value
        self.xChanged.emit(self._x_val)

    # getter
    def get_y_val(self):
        return self._y_val

    # setter
    def set_y_val(self, value):
        self._y_val = value
        self.yChanged.emit(self._y_val)

    # getter
    def get_dim(self):
        return self._dim

    # setter
    def set_dim(self, value):
        self._dim = value

    # getter
    def get_custom_color(self):
        return self._custom_color

    # setter
    def set_custom_color(self, value):
        self._custom_color = value

    # getter
    def get_eye(self):
        return self._eye

    # setter
    def set_eye(self, value):
        self._eye = value

    # getter
    def get_sub_id(self):
        return self._sub_id

    # setter
    def set_sub_id(self, value):
        self._sub_id = value

    # getter
    def get_save_loc(self):
        return self._save_loc

    # setter
    def set_save_loc(self, value):
        self._save_loc = value

    # getter
    def get_device(self):
        return self._device

    # setter
    def set_device(self, value):
        self._device = value

    # getter
    def get_left_label(self):
        return self._left_label

    # setter
    def set_left_label(self, value):
        self._left_label = value

    # getter
    def get_right_label(self):
        return self._right_label

    # setter
    def set_right_label(self, value):
        self._right_label = value

    # getter
    def get_current_fov(self):
        return self._current_fov

    # setter
    def set_current_fov(self, value):
        self._current_fov = value

    # getter
    def get_shape(self):
        return self._shape

    # setter
    def set_shape(self, value):
        self._shape = value
        self.shapeChanged.emit(self._shape)

    # getter
    def get_size(self):
        return self._size

    # setter
    def set_size(self, value):
        self._size = value

    # getter
    def get_thickness(self):
        return self._size

    # setter
    def set_thickness(self, value):
        self._size = value

    # getter
    def get_center_x(self):
        return self._center_x

    # setter
    def set_center_x(self, value):
        self._center_x = value

    def get_center_y(self):
        return self._center_y

    # setter
    def set_center_y(self, value):
        self._center_y = value

    # getter
    def get_center_x_og(self):
        return self._center_x_og

    # setter
    def set_center_x_og(self, value):
        self._center_x_og = value

    def get_center_y_og(self):
        return self._center_y_og

    # setter
    def set_center_y_og(self, value):
        self._center_y_og = value

    def get_target_vis(self):
        return self._target_vis

    # setter
    def set_target_vis(self, value):
        self._target_vis = value

    # getter
    def get_center_x_grid(self):
        return self._center_x_grid

    # setter
    def set_center_x_grid(self, value):
        self._center_x_grid = value

    def get_center_y_grid(self):
        return self._center_y_grid

    # setter
    def set_center_y_grid(self, value):
        self._center_y_grid = value

    # getter
    def get_center_x_og_grid(self):
        return self._center_x_og_grid

    # setter
    def set_center_x_og_grid(self, value):
        self._center_x_og_grid = value

    def get_center_y_og_grid(self):
        return self._center_y_og_grid

    # setter
    def set_center_y_og_grid(self, value):
        self._center_y_og_grid = value

    def get_grid_mult(self):
        return self._grid_mult

    # setter
    def set_grid_mult(self, value):
        self._grid_mult = value

    # getter
    def get_screen_ppd(self):
        return self._screen_ppd

    # setter
    def set_screen_ppd(self, value):
        self._screen_ppd = value

    # getter
    def get_grid_vis(self):
        return self._grid_vis

    # setter
    def set_grid_vis(self, value):
        self._grid_vis = value

    # getter
    def get_control_ref(self):
        return self._control_ref

    # setter
    def set_control_ref(self, value):
        self._control_ref = value

    # getter
    def get_notes_ref(self):
        return self._notes_ref

    # setter
    def set_notes_ref(self, value):
        self._notes_ref = value

    # getter
    def get_notes_entry(self):
        return self._notes_entry

    # setter
    def set_notes_entry(self, value):
        self._notes_entry = value

    # getter
    def get_video_list_entry(self):
        return self._video_list_entry

    # setter
    def set_video_list_entry(self, value):
        self._video_list_entry = value

    # getter
    def get_recvQ(self):
        return self._recvQ

    # setter
    def set_recvQ(self, value):
        self._recvQ = value

    # getter
    def get_vid_num(self):
        return self._vid_num

    # setter
    def set_vid_num(self, value):
        self._vid_num = value

    # getter
    def get_fov_list(self):
        return self._fov_list

    # setter
    def set_fov_list(self, value):
        self._fov_list = value

    # getter
    def get_ref_point(self):
        return self._ref_point

    # setter
    def set_ref_point(self, value):
        self._ref_point = value

    # getter
    def get_x_ref(self):
        return self._x_ref

    # setter
    def set_x_ref(self, value):
        self._x_ref = value

    # getter
    def get_y_ref(self):
        return self._y_ref

    # setter
    def set_y_ref(self, value):
        self._y_ref = value

    # getter
    def get_image_path(self):
        return self._image_path

    # setter
    def set_image_path(self, value):
        self._image_path = value

    # creating property objects
    # sourced from tabs
    animation_speed = QtCore.Property(float, get_animation_speed_val, set_animation_speed_val)
    x_pos_deg = QtCore.Property(int, get_x_val, set_x_val, notify=xChanged)
    y_pos_deg = QtCore.Property(int, get_y_val, set_y_val, notify=yChanged)
    dim = QtCore.Property(str, get_dim, set_dim)
    target_color = QtCore.Property(QtGui.QColor, get_custom_color, set_custom_color)  # QtGui.QColor('green')
    eye = QtCore.Property(str, get_eye, set_eye)
    fov = QtCore.Property(bool, get_current_fov, set_current_fov)
    target_shape = QtCore.Property(Target, get_shape, set_shape, notify=shapeChanged)
    target_size = QtCore.Property(float, get_size, set_size)
    target_thickness = QtCore.Property(float, get_thickness, set_thickness)

    fixation_target_ppd = QtCore.Property(float, get_screen_ppd, set_screen_ppd)
    fov_list = QtCore.Property(bool, get_fov_list, set_fov_list)
    ref_point = QtCore.Property(bool, get_ref_point, set_ref_point)
    x_ref = QtCore.Property(bool, get_x_ref, set_x_ref)
    y_ref = QtCore.Property(bool, get_y_ref, set_y_ref)



if __name__ == "__main__":
    var = StatusVariables()
    # test
    var.horz = 22.5
    print(var.horz)
