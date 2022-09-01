
import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import (QTableWidget,QStyledItemDelegate, QHeaderView, QAbstractScrollArea, QTableWidgetItem)
import configparser
import pandas as pd
from threading import Timer
import threading
import pdfrw

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

class NuclearNotes(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # read in the config file
        self.config = configparser.ConfigParser()
        self.config.read('C:\\Users\\6794grieshj\\Documents\\GitHub\\Fixation_GUI_Qt\\test_settings.ini')
        self.notes_fname = 'test_file.xlsx'
        self.horizontal_table_headers = None

        self.layout = QtWidgets.QVBoxLayout(self)

        # fake record button to test adding more rows when a video is recorded
        self.button = QtWidgets.QPushButton("FakeRecordButton")
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.addRow)

        # https: // stackoverflow.com / questions / 54612127 / how - to - i - set - the - size - hint -
        # for -a - qtablewidget - in -python
        # make the table and set it up to be formatted nicely
        self.table_widget = self.constructTable()
        self.table_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table_widget, stretch=True)

        # start notes saving
        self.template_pdf = pdfrw.PdfReader(self.config.get("test", "notes_pdf_template"))
        self.testPop = []
        self.saveNotes()
        self.test = 0

    def constructTable(self):
        # https://stackoverflow.com/questions/4097139/reading-array-from-config-file-in-python
        self.horizontal_table_headers = self.config.get("test", "horizontal_table_headers").split("/")
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
        self.row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(self.row_count)
        self.memory = self.config.get("test", "memory_columns").split("/")
        length = len(self.memory)-1

        # Creating items for each cell in the table as it is created & setting text alignment to center
        for i in range(len(self.horizontal_table_headers)):
            item = QTableWidgetItem()
            self.table_widget.setItem(self.row_count, i, item)
            self.table_widget.item(self.row_count, i).setTextAlignment(5)

        # populating columns --simulation for now. will need to get this info from savior/grid later
        self.testPop = ["0", "(1,1)", "2.0 x 2.0", "OD"]
        for i in range(len(self.testPop)):
            self.table_widget.item(self.row_count, i).setText(self.testPop[i])

        # column memory - currently needs to have all memory columns next to each other
        try:
            for i in range(int(self.memory[0]), int(self.memory[len(self.memory)-1])+1):
                self.table_widget.item(self.row_count, i).setText(str(self.table_widget.item(self.row_count-1, i).text()))
        except AttributeError:
            pass

    @QtCore.Slot()
    def saveNotes(self):

        # create pandas dataframe
        df = pd.DataFrame(columns=self.horizontal_table_headers)

        # populate dataframe with the table information
        for col in range(self.table_widget.columnCount()):
            for row in range(self.table_widget.rowCount()):
                try:
                    df.at[row, self.horizontal_table_headers[col]] = str(self.table_widget.item(row, col).text())
                except AttributeError:
                    pass

        # save the dataframe to an excel file
        df.to_excel(self.notes_fname, index=False)

        # don't try to start saving notes to pdf if no videos have been taken yet
        if len(self.testPop) != 0:

            # Names of the fields for Notes Pdf template. Should be at least partially sourced from the config file!!!!!!!!!!!!!!
            eye = self.testPop[0]
            FOV = 'FOV ' + self.testPop[0]
            locNotes = 'Location  Notes' + self.testPop[0]
            focus = 'Focus ' + self.testPop[0]
            # print(focus)
            conf = 'Conf' + self.testPop[0]
            dir = 'Dir' + self.testPop[0]
            ref = 'Ref' + self.testPop[0]
            vis = 'Vis' + self.testPop[0]

            # this is the dictionary that has all the values that will be put into the pdf. Need to get this on some kind of loop i believe
            data_dict = {
                eye: self.testPop[3],
                FOV: self.testPop[2],
                locNotes: self.testPop[1],
                focus: self.table_widget.item(0, 5).text(),
                conf: 'test',
                dir: 'test',
                ref: 'test',
                vis: 'test'
            }

            # code that puts the data into the pdf and saves it
            for page in self.template_pdf.pages:
                annotations = page[ANNOT_KEY]
                for annotation in annotations:
                    if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                        if annotation[ANNOT_FIELD_KEY]:
                            key = annotation[ANNOT_FIELD_KEY][1:-1]
                            if key in data_dict.keys():
                                if type(data_dict[key]) == bool:
                                    if data_dict[key] == True:
                                        annotation.update(pdfrw.PdfDict(
                                            AS=pdfrw.PdfName('Yes')))
                                else:
                                    annotation.update(
                                        pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                                    )
                                    annotation.update(pdfrw.PdfDict(AP=''))
            self.template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
            pdfrw.PdfWriter().write('testNotesPdf.pdf', self.template_pdf)

        # start timer to automatically save notes every 5 seconds
        threading.Timer(5.0, self.saveNotes).start()


class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        # print('createEditor event fired')
        return


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = NuclearNotes()
    widget.show()
    widget.resize(800, 600)
    sys.exit(app.exec())
