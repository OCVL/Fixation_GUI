import configparser
import os

import pandas
from PySide6 import QtCore, QtGui


# using property class
class Variables:
    def __init__(self, animation_speed_val=None, x_val=0, y_val=0, dim=None, savior_FOVs=None, \
                 custom_color=None, eye='OX', sub_id='XXXXX', save_loc=None, device=None, left_label=None,
                 right_label=None, current_fov='0.0 x 0.0', shape=None, size=None, center_x=None, center_y=None,
                 center_x_og=None, center_y_og=None, target_vis=None, stimulus_imaging=None,
                 center_x_grid=None, center_y_grid=None, center_x_og_grid=None, center_y_og_grid=None, grid_mult=23.3,
                 screen_ppd=None, grid_vis=None, control_ref=None, notes_ref=None, notes_entry="", video_list_entry=None,
                 recvQ=None, vid_num=None, fov_list=[], ref_point=False, x_ref= None, y_ref=None, image_path=None):
        self.animation_speed_val = animation_speed_val
        self.x_val = x_val
        self.y_val = y_val
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
        self.shape = shape
        self.size = size
        self.center_x = center_x
        self.center_y = center_y
        self.center_x_og = center_x_og
        self.center_y_og = center_y_og
        self.target_vis = target_vis
        self.stimulus_imaging = stimulus_imaging
        self.center_x_grid = center_x_grid
        self.center_y_grid = center_y_grid
        self.center_x_og_grid = center_x_og_grid
        self.center_y_og_grid = center_y_og_grid
        self.grid_mult = grid_mult
        self.screen_ppd = screen_ppd
        self.grid_vis = grid_vis
        self.control_ref = control_ref
        self.notes_ref = notes_ref
        self.notes_entry = notes_entry
        self.video_list_entry = video_list_entry
        self.recvQ = recvQ
        self.vid_num = vid_num
        self.fov_list = fov_list
        self.ref_point = ref_point
        self.x_ref = x_ref
        self.y_ref = y_ref
        self.image_path = image_path


        # configuration file set up
        self.config = configparser.ConfigParser()
        self.config_name = os.getcwd() + "\\test_settings.ini"
        self.config.read(self.config_name)

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

    # getter
    def get_y_val(self):
        return self._y_val

    # setter
    def set_y_val(self, value):
        self._y_val = value

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

    # getter
    def get_shape(self):
        return self._shape

    # setter
    def set_shape(self, value):
        self._shape = value

    # getter
    def get_size(self):
        return self._size

    # setter
    def set_size(self, value):
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
    animation_speed_val = QtCore.Property(float, get_animation_speed_val, set_animation_speed_val)
    x_val = QtCore.Property(int, get_x_val, set_x_val)
    y_val = QtCore.Property(int, get_y_val, set_y_val)
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
    shape = QtCore.Property(bool, get_shape, set_shape)
    size = QtCore.Property(bool, get_size, set_size)
    center_x = QtCore.Property(bool, get_center_x, set_center_x)
    center_y = QtCore.Property(bool, get_center_y, set_center_y)
    center_x_og = QtCore.Property(bool, get_center_x_og, set_center_x_og)
    center_y_og = QtCore.Property(bool, get_center_y_og, set_center_y_og)
    target_vis = QtCore.Property(bool, get_target_vis, set_target_vis)
    stimulus_imaging = QtCore.Property(bool, get_stimulus_imaging, set_stimulus_imaging)
    center_x_grid = QtCore.Property(bool, get_center_x_grid, set_center_x_grid)
    center_y_grid = QtCore.Property(bool, get_center_y_grid, set_center_y_grid)
    center_x_og_grid = QtCore.Property(bool, get_center_x_og_grid, set_center_x_og_grid)
    center_y_og_grid = QtCore.Property(bool, get_center_y_og_grid, set_center_y_og_grid)
    grid_mult = QtCore.Property(bool, get_grid_mult, set_grid_mult)
    screen_ppd = QtCore.Property(bool, get_screen_ppd, set_screen_ppd)
    grid_vis = QtCore.Property(bool, get_grid_vis, set_grid_vis)
    control_ref = QtCore.Property(bool, get_control_ref, set_control_ref)
    notes_ref = QtCore.Property(bool, get_notes_ref, set_notes_ref)
    notes_entry = QtCore.Property(bool, get_notes_entry, set_notes_entry)
    video_list_entry = QtCore.Property(bool, get_video_list_entry, set_video_list_entry)
    recvQ = QtCore.Property(bool, get_recvQ, set_recvQ)
    vid_num = QtCore.Property(bool, get_vid_num, set_vid_num)
    fov_list = QtCore.Property(bool, get_fov_list, set_fov_list)
    ref_point = QtCore.Property(bool, get_ref_point, set_ref_point)
    x_ref = QtCore.Property(bool, get_x_ref, set_x_ref)
    y_ref = QtCore.Property(bool, get_y_ref, set_y_ref)
    image_path = QtCore.Property(bool, get_image_path, set_image_path)


if __name__ == "__main__":
    var = Variables()
    # test
    var.horz = 22.5
    print(var.horz)
