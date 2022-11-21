import configparser
import os
from PySide6 import QtCore, QtGui


# using property class
class Variables:
    def __init__(self, animation_speed_val=None, horz_val=None, vert_val=None, dim=None, savior_FOVs=None, \
                 custom_color=QtGui.QColor('green'), eye='OX', sub_id='XXXXX', save_loc=None, device=None, left_label=None,
                 right_label=None, current_fov='1.0 x 1.0'):
        self.animation_speed_val = animation_speed_val
        self.horz_val = horz_val
        self.vert_val = vert_val
        self.dim = dim
        self.savior_FOVs = savior_FOVs
        self.custom_color = custom_color
        self.eye = eye
        self.sub_id = sub_id
        self.save_loc = save_loc
        self.device = device
        self.left_label = left_label
        self.right_label = right_label
        self.current_fov = current_fov

        # configuration file set up
        self.config = configparser.ConfigParser()
        self.config_name = os.getcwd() + "\\test_settings.ini"


    # getter
    def get_animation_speed_val(self):
        return self._animation_speed_val

    # setter
    def set_animation_speed_val(self, value):
        self._animation_speed_val = value

    # getter
    def get_horz_val(self):
        return self._horz_val

    # setter
    def set_horz_val(self, value):
        self._horz_val = value

    # getter
    def get_vert_val(self):
        return self._vert_val

    # setter
    def set_vert_val(self, value):
        self._vert_val = value

    # getter
    def get_dim(self):
        return self._dim

    # setter
    def set_dim(self, value):
        self._dim = value

    # getter
    def get_savior_FOVs(self):
        return self._savior_FOVs

    # setter
    def set_savior_FOVs(self, value):
        self._savior_FOVs = value

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

    # creating property objects
    # sourced from tabs
    animation_speed_val = QtCore.Property(float, get_animation_speed_val, set_animation_speed_val)
    horz_val = QtCore.Property(int, get_horz_val, set_horz_val)
    vert_val = QtCore.Property(int, get_vert_val, set_vert_val)
    dim = QtCore.Property(str, get_dim, set_dim)
    savior_FOVs = QtCore.Property(str, get_savior_FOVs, set_savior_FOVs)
    custom_color = QtCore.Property(QtGui.QColor, get_custom_color, set_custom_color)  # QtGui.QColor('green')
    eye = QtCore.Property(str, get_eye, set_eye)
    sub_id = QtCore.Property(str, get_sub_id, set_sub_id)
    save_loc = QtCore.Property(str, get_save_loc, set_save_loc)
    device = QtCore.Property(str, get_device, set_device)
    left_label = QtCore.Property(str, get_left_label, set_left_label)
    right_label = QtCore.Property(str, get_right_label, set_right_label)
    fov = QtCore.Property(bool, get_current_fov, set_current_fov)


if __name__ == "__main__":
    var = Variables()
    # test
    var.horz = 22.5
    print(var.horz)
