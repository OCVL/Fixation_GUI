from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen


class NuclearTarget(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        display_monitor = 1
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)

        #send it to a different monitor and make full screen
        monitors = QScreen.virtualSiblings(self.screen())
        monitor = monitors[display_monitor].availableGeometry()
        self.move(monitor.left(), monitor.top())
        self.showFullScreen()
