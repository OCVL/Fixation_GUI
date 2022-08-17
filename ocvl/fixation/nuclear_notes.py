
import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import (QTableWidget,QStyledItemDelegate, QHeaderView, QAbstractScrollArea)
import configparser

class NuclearNotes(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        config = configparser.ConfigParser()
        config.read('C:\\Users\\6794grieshj\\Documents\\GitHub\\Fixation_GUI_Qt\\test_settings.ini')
        # https://stackoverflow.com/questions/4097139/reading-array-from-config-file-in-python
        horizontal_table_headers = config.get("test", "horizontal_table_headers").split("/")

        self.button = QtWidgets.QPushButton("FakeRecordButton")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.addRow)
        self.table_widget = self.constructTable(horizontal_table_headers)
        self.table_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_widget.setAlternatingRowColors(True)
        self.layout.addWidget(self.table_widget, stretch=True)
        # https: // stackoverflow.com / questions / 54612127 / how - to - i - set - the - size - hint -
        # for -a - qtablewidget - in -python
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def constructTable(self, headers):
        table_columns = len(headers)
        # self.column_width = round(766/self.table_columns)
        table_rows = 0  # should make this a variable that grows

        table = QTableWidget()

        table.setRowCount(table_rows)
        # https: // stackoverflow.com / questions / 578371 / hiding - row - labels
        table.verticalHeader().setVisible(False)
        table.setColumnCount(table_columns)
        table.setHorizontalHeaderLabels(
            headers)  # should probably source these from init/preferences file

        delegate = ReadOnlyDelegate(self)
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
