import sys
from datetime import datetime
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QEvent
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (QTableWidget,QStyledItemDelegate, QHeaderView, QAbstractScrollArea, QTableWidgetItem)
import pandas as pd
import pdfrw
from pandas import concat


ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'
class NuclearNotes(QtWidgets.QWidget):
    """
    Class for the notes panel
    """
    def __init__(self, var):
        super().__init__()

        self.var = var

        self.horizontal_table_headers = None

        self.layout = QtWidgets.QVBoxLayout(self)

        # https://stackoverflow.com/questions/54612127/how-to-i-set-the-size-hint-for-a-qtablewidget-in-python
        # make the table and set it up to be formatted nicely
        self.table_widget = self.constructTable()
        self.table_widget.installEventFilter(self)
        self.table_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.table_widget.setAlternatingRowColors(True)
        # Added so that the notes table doesn't interfere with the location moving
        self.table_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.layout.addWidget(self.table_widget, stretch=True)

        # start notes saving
        self.test = 0
        self.count = 0


        # create pandas dataframe
        self.loc_df = pd.DataFrame(columns=['v0.3', 'Location', 'Horizontal FOV', 'Vertical FOV'])

    def constructTable(self):
        """
        Constucts table
        :return:
        """
        # https://stackoverflow.com/questions/4097139/reading-array-from-config-file-in-python
        self.horizontal_table_headers = self.var.config.get( "horizontal_table_headers").split("/")
        table_columns = len(self.horizontal_table_headers)
        table_rows = 0

        table = QTableWidget()

        # set up rows
        table.setRowCount(table_rows)
        # https: // stackoverflow.com / questions / 578371 / hiding - row - labels
        table.verticalHeader().setVisible(False)

        # set up columns
        table.setColumnCount(table_columns)
        table.setHorizontalHeaderLabels(
            self.horizontal_table_headers)
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)

        # delegate will be used to disable editing of columns
        delegate = ReadOnlyDelegate(self)
        # these columns will not be editable -- could be pulled from config file
        table.setItemDelegateForColumn(0, delegate)
        table.setItemDelegateForColumn(1, delegate)
        table.setItemDelegateForColumn(2, delegate)

        return table

    def eventFilter(self, source, event, keyboard=None):
        """
        clears the focus on the text boxe when up/down arrow keys are pressed
        :param source: the source of the event
        :param event: the event
        :return:
        """

        if (event.type() == QtCore.QEvent.KeyPress and
                    event.key() in (QtCore.Qt.Key_Up, QtCore.Qt.Key_Down)):
            # this is the only order I've gotten it to work decently
            self.table_widget.focusPreviousChild()
            self.table_widget.clearFocus()

        return super().eventFilter(source, event)

    @QtCore.Slot()
    def addRow(self):
        """
        Adds a row to the notes table
        :return:
        """
        # https: // stackoverflow.com / questions / 6957943 / how - to - add - new - row - to - existing - qtablewidget
        self.row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(0)  # self.row_count
        self.memory = self.var.config.get( "memory_columns").split("/")
        length = len(self.memory)-1

        # Creating items for each cell in the table as it is created & setting text alignment to center
        for i in range(len(self.horizontal_table_headers)):
            item = QTableWidgetItem()
            self.table_widget.setItem(0, i, item)  # self.row_count
            self.table_widget.item(0, i).setTextAlignment(5)  # self.row_count


        self.current_location = "(" + str(self.var.x_pos) + "," + str(self.var.y_val) + ")"
        self.testPop = [self.var.vid_num, self.current_location, self.var.current_fov, self.var.notes_entry]
        for i in range(len(self.testPop)):
            self.table_widget.item(0, i).setText(self.testPop[i])  # self.row_count

        # column memory - currently needs to have all memory columns next to each other
        try:
            for i in range(int(self.memory[0]), int(self.memory[len(self.memory)-1])+1):
                self.table_widget.item(0, i).setText(str(self.table_widget.item(1, i).text()))
        except AttributeError:
            pass
        self.saveNotes()
        self.saveLocations()
        self.count = self.count+1
        # add video entry to the list to be stored for painting on grid
        self.var.video_list_entry = [self.var.vid_num, self.current_location, self.var.current_fov]


class ReadOnlyDelegate(QStyledItemDelegate):
    """
    Class to make things read only
    """
    def createEditor(self, parent, option, index):
        return


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # can't run on its own unless you hard code the config file path as an argument below
    widget = NuclearNotes()
    widget.show()
    widget.resize(800, 600)
    sys.exit(app.exec())
