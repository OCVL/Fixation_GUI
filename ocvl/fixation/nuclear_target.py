
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtGui import QScreen, QPainter
from ocvl.fixation.targets import *

class NuclearTarget(QGraphicsView):

    # maybe want to put this in the config file
    # The number of ppd of the screen we'll be projecting to (e.g. Lightcrafter, Projector, etc).
    SCREEN_PPD = 20

    def __init__(self, var):
        super().__init__()

        self.scene = QGraphicsScene()

        self.setScene(self.scene)

        self.var = var
        display_monitor = 0
        #send it to a different monitor and make full screen
        monitors = QScreen.virtualSiblings(self.screen())
        monitor = monitors[display_monitor].availableGeometry()
        self.move(monitor.left(), monitor.top())

        self.init = 1
        defaults = self.var.config.get("test", "fixation_default").split("/")

        if defaults[0] == 'on':
            self.var.target_vis = True
        else:
            self.var.target_vis = False

        self.var.center_x = QPainter(self).window().width() / 2
        self.var.center_y = QPainter(self).window().height() / 2

        self.current_target = self.var.shape
        self.scene.addItem(self.current_target)
        self.var.shapeChanged.connect(self.setTarget)
        self.setFrameStyle(0)

    def setTarget(self, target: Target):
        self.scene.clear()
        self.viewport().update()

        self.current_shape = target

        self.scene.addItem(target)

        return target

