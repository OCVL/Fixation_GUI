import sys

import PySide6
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QEvent
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (QTableWidget,QStyledItemDelegate, QHeaderView, QAbstractScrollArea, QTableWidgetItem)
import pandas as pd
import pdfrw

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
        self.notes_fname = 'test_notes.xlsx'  # will need to use config file to get the convention and then fill in
        self.locations_fname = 'test_locations.xlsx'
        self.horizontal_table_headers = None

        self.layout = QtWidgets.QVBoxLayout(self)

        # https://stackoverflow.com/questions/54612127/how-to-i-set-the-size-hint-for-a-qtablewidget-in-python
        # make the table and set it up to be formatted nicely
        self.table_widget = self.constructTable()
        self.table_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.table_widget.setAlternatingRowColors(True)
        # Added so that the notes table doesn't interfere with the location moving
        self.table_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.layout.addWidget(self.table_widget, stretch=True)

        # start notes saving
        self.template_pdf = pdfrw.PdfReader(self.var.config.get("test", "notes_pdf_template"))
        self.notes_fields = self.var.config.get("test", "notes_fields").split("/")
        self.testPop = []
        self.saveNotes()
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
        self.horizontal_table_headers = self.var.config.get("test", "horizontal_table_headers").split("/")
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
        table.itemSelectionChanged.connect(self.saveNotes)

        return table

    @QtCore.Slot()
    def addRow(self):
        """
        Adds a row to the notes table
        :return:
        """
        # https: // stackoverflow.com / questions / 6957943 / how - to - add - new - row - to - existing - qtablewidget
        self.row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(0)  # self.row_count
        self.memory = self.var.config.get("test", "memory_columns").split("/")
        length = len(self.memory)-1

        # Creating items for each cell in the table as it is created & setting text alignment to center
        for i in range(len(self.horizontal_table_headers)):
            item = QTableWidgetItem()
            self.table_widget.setItem(0, i, item)  # self.row_count
            self.table_widget.item(0, i).setTextAlignment(5)  # self.row_count

        # populating columns --simulation for now. will need to get this info from savior/grid later
        # self.var.current_fov = "1.0 x 1.0"
        self.current_location = "(" + str(self.var.x_val) + "," + str(self.var.y_val) + ")"
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

    @QtCore.Slot()
    def saveNotes(self):
        """
        Saves the notes table
        :return:
        """
        # create pandas dataframe
        self.df = pd.DataFrame(columns=self.horizontal_table_headers)

        # populate dataframe with the table information
        for col in range(self.table_widget.columnCount()):
            for row in range(self.table_widget.rowCount()):
                try:
                    self.df.at[row, self.horizontal_table_headers[col]] = str(self.table_widget.item(row, col).text())
                except AttributeError:
                    pass

        # flip dataframe indices so that it is in chronological order for the csv
        # https://stackoverflow.com/questions/20444087/right-way-to-reverse-a-pandas-dataframe
        self.df = self.df.iloc[::-1]
        # save the dataframe to an Excel file
        self.df.to_excel(self.notes_fname, index=False)

        # code that was created to save notes to pdf - maybe can reuse for the upon exit/conversion script
        # # don't try to start saving notes to pdf if no videos have been taken yet
        # if len(self.testPop) != 0:
        #
        #     # Names of the fields for Notes Pdf template. Should be at least partially sourced from the config file!!!!!!!!!!!!!!
        #     eye = self.testPop[0]
        #     FOV =  self.notes_fields[0] + self.testPop[0]
        #     locNotes = self.notes_fields[1] + self.testPop[0]
        #     focus = self.notes_fields[2] + self.testPop[0]
        #     # print(focus)
        #     conf = self.notes_fields[3] + self.testPop[0]
        #     dir = self.notes_fields[4] + self.testPop[0]
        #     ref = self.notes_fields[5] + self.testPop[0]
        #     vis = self.notes_fields[6] + self.testPop[0]
        #
        #     # this is the dictionary that has all the values that will be put into the pdf. currently has problems bc video number isn't changing
        #     for z in range(0, self.table_widget.rowCount()):
        #         data_dict = {
        #             eye: self.testPop[3],
        #             FOV: self.testPop[2],
        #             locNotes: self.testPop[1] + '; ' + self.table_widget.item(z, 4).text(),
        #             focus: self.table_widget.item(z, 5).text(), # will need to find a way to have these in order of what it is agnostically!!!!!!!!!!!!!!!!!!!
        #             conf: self.table_widget.item(z, 6).text(),
        #             dir: self.table_widget.item(z, 7).text(),
        #             ref: self.table_widget.item(z, 8).text(),
        #             vis: self.table_widget.item(z, 9).text(),
        #         }
        #
        #     # code that puts the data into the pdf and saves it
        #     for page in self.template_pdf.pages:
        #         annotations = page[ANNOT_KEY]
        #         for annotation in annotations:
        #             if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
        #                 if annotation[ANNOT_FIELD_KEY]:
        #                     key = annotation[ANNOT_FIELD_KEY][1:-1]
        #                     if key in data_dict.keys():
        #                         if type(data_dict[key]) == bool:
        #                             if data_dict[key] == True:
        #                                 annotation.update(pdfrw.PdfDict(
        #                                     AS=pdfrw.PdfName('Yes')))
        #                         else:
        #                             annotation.update(
        #                                 pdfrw.PdfDict(V='{}'.format(data_dict[key]))
        #                             )
        #                             annotation.update(pdfrw.PdfDict(AP=''))
        # self.template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        # pdfrw.PdfWriter().write('testNotesPdf.pdf', self.template_pdf)  # will need to have this not be hard coded later on!!!!!!!!!!!!!!!!!!

    def saveLocations(self):
        '''
        Saves the locations csv file
        :return:
        '''
        vid_num = []
        loc = []
        fov = []

        vid_num = self.df.get('Video #')
        vid_num = int(vid_num[0])
        loc = self.df.get('Location')
        loc = loc[0].replace('(', '').replace(')', '')
        fov = self.df.get('FOV')
        fov = fov[0].split(' ')
        hfov = float(fov[0])
        vfov = float(fov[2])

        data = {
            'v0.3': vid_num,
            'Location': loc,
            'Horizontal FOV': hfov,
            'Vertical FOV': vfov
        }

        self.loc_df = self.loc_df.append(data, ignore_index=True)

        # save the dataframe to an Excel file
        self.loc_df.to_excel(self.locations_fname, index=False)


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
