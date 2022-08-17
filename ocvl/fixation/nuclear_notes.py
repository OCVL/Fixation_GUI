
import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import (QTableWidget,QStyledItemDelegate, QHeaderView, QAbstractScrollArea)
import configparser

class NuclearNotes(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # read in the config file
        config = configparser.ConfigParser()
        config.read('C:\\Users\\6794grieshj\\Documents\\GitHub\\Fixation_GUI_Qt\\test_settings.ini')

        self.layout = QtWidgets.QVBoxLayout(self)

        # fake record button to test adding more rows when a video is recorded
        self.button = QtWidgets.QPushButton("FakeRecordButton")
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.addRow)

        # https: // stackoverflow.com / questions / 54612127 / how - to - i - set - the - size - hint -
        # for -a - qtablewidget - in -python
        # make the table and set it up to be formatted nicely
        self.table_widget = self.constructTable(config)
        self.table_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table_widget, stretch=True)

    def constructTable(self, config):
        # https://stackoverflow.com/questions/4097139/reading-array-from-config-file-in-python
        horizontal_table_headers = config.get("test", "horizontal_table_headers").split("/")
        table_columns = len(horizontal_table_headers)
        table_rows = 0

        table = QTableWidget()

        # set up rows
        table.setRowCount(table_rows)
        # https: // stackoverflow.com / questions / 578371 / hiding - row - labels
        table.verticalHeader().setVisible(False)

        # set up columns
        table.setColumnCount(table_columns)
        table.setHorizontalHeaderLabels(
            horizontal_table_headers)  # should probably source these from init/preferences file

        # delegate will be used to disable editing of columns
        delegate = ReadOnlyDelegate(self)
        # these columns will not be editable -- could be pulled from config file
        table.setItemDelegateForColumn(0, delegate)
        table.setItemDelegateForColumn(1, delegate)
        table.setItemDelegateForColumn(2, delegate)
        table.setItemDelegateForColumn(3, delegate)

        return table

    @QtCore.Slot()
    def addRow(self):
        # https: // stackoverflow.com / questions / 6957943 / how - to - add - new - row - to - existing - qtablewidget
        self.table_widget.insertRow(self.table_widget.rowCount())

class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        print('createEditor event fired')
        return


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = NuclearNotes()
    widget.show()
    widget.resize(800, 600)
    sys.exit(app.exec())
