from PySide6 import QtCore


# using property class
class Variables:
    def __init__(self, horz=0, vert=0):
        self.horz = horz
        self.vert = vert

    # getter
    def get_horz(self):
        return self._horz

    # setter
    def set_horz(self, value):
        self._horz = value

    # getter
    def get_vert(self):
        return self._vert

    # setter
    def set_vert(self, value):
        self._vert = value

    # creating property objects
    horz = QtCore.Property(float, get_horz, set_horz)
    vert = QtCore.Property(float, get_vert, set_vert)


if __name__ == "__main__":
    var = Variables()
    var.horz = 22.5
    print(var.horz)
