import sys
import json
import logging
from PyQt6 import QtWidgets, uic
from controllers.odbc import (
    ODBCPostgresql,
    ODBCSQLite,
)
from PyQt6Extended import (
    QMainWindowExtended,
    QWidgetExtended,
    QDialogExtended,
    ) 
from PyQt6.QtGui import QPalette, QColor
from models.constants import *

logger = logging.getLogger('qt-queries')
logger.setLevel(logging.INFO)

# Services
# ----------------------------------------------------------------------------

def get_list_conn():
    with open('connections.json', 'r') as f:
        conns = json.loads(f.read() or '{}')
        for i in conns.items():
            yield i

def save_conn(name, host, port, user, pswd, dbname, driver_name):
    driver_name = LABEL_TO_SQL_DRIVER[driver_name]
    with open('connections.json', 'r') as f:
        conns = json.loads(f.read() or '{}')
    conns[name] = {
            'host': host,
            'port': port,
            'user': user,
            'pswd': pswd,
            'database': dbname,
            'driver_name': driver_name,
        }
    with open('connections.json', 'w') as f:
        f.write(json.dumps(conns, indent=2))

# UI
# ----------------------------------------------------------------------------


class MainWindow(QMainWindowExtended):

    template_path = 'views/main.ui'

    def openNewConnDialog(self, *args, **kwargs):
        w = NewConnQDialog()
        w.exec()

    def executeQuery(self, *args, **kwargs):
        conn_name = self.get_combobox_selected_text('comboBoxConnections')
        print(conn_name)
        sql_query = self.get_qplaintextedit_text('plainTextEditQueries')
        print(sql_query)
        if len(sql_query):
            odbc_conn = ODBCSQLite(conn_name)
            odbc_conn.connect()
            query_res = odbc_conn.query(sql_query)
            print(query_res)
            odbc_conn.close()

    def newQuerySessionTab(self, *args, **kwargs):
        tab = self.get_qtabwidget('tabWidgetQueryEditor')
        page = QuerySessionTab()
        tab_count = tab.count() + 1
        new_tab_idx = tab.addTab(page, f'Query {tab_count}')
        tab.setCurrentIndex(new_tab_idx)


class QuerySessionTab(QWidgetExtended):

    template_path = 'views/query_session_tab.ui'

    def bind_data(self):
        self.label_qcombobox_available_conns = 'comboBoxAvailableConns'
        conns = self.findChild(
                QtWidgets.QComboBox, self.label_qcombobox_available_conns)
        for i, conn in enumerate(get_list_conn()):
            conn_name = conn[0]
            conns.insertItem(i, conn_name)
        editor = self.get_plaintextedit('plainTextEditQueryEditor')
        editor.setFocus()  # TODO why is this focus not working?

    def selectedConnChanged(self, idx):
        conns = self.findChild(
                QtWidgets.QComboBox, self.label_qcombobox_available_conns)
        conn_name = conns.itemText(idx)
        print(conn_name)

    def executeQuery(self, *args, **kwargs):
        conn_name = self.get_combobox_selected_text(
                self.label_qcombobox_available_conns)
        print(conn_name)
        sql_query = self.get_qplaintextedit_text('plainTextEditQueryEditor')
        print(sql_query)
        if len(sql_query):
            odbc_conn = ODBCSQLite(conn_name)
            odbc_conn.connect()
            try:
                query_cols, query_res = odbc_conn.query(sql_query)
                query_res = list(query_res)
                print(query_res)
                odbc_conn.close()
                self.bind_query_result_to_table(query_cols, query_res)
            except Exception as ex:
                errors = self.get_textedit('textEditQueryError')
                errors.setText(str(ex))
                tab = self.get_tab('tabWidgetPostQueryExecution')
                tab_error = tab.findChild(QtWidgets.QWidget, 'tabQueryError')
                tab_error.setFocus()
                print(ex)

    def bind_query_result_to_table(self, query_cols, query_result):
        table = self.get_qtablewidget('tableWidgetQueryResult')
        table.setRowCount(len(query_result))
        table.setColumnCount(len(query_result[0]))
        for i, col_info in enumerate(query_cols):
            table.setHorizontalHeaderItem(
                i,
                QtWidgets.QTableWidgetItem(f'{col_info[0]}'),
                )
        for row_idx, row in enumerate(query_result):
            print(row_idx, row)
            for col_idx, col in enumerate(row):
                col = str(col)
                table.setItem(
                    row_idx, col_idx, QtWidgets.QTableWidgetItem(col))

class NewConnQDialog(QDialogExtended):

    template_path = 'views/new_connections.ui'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind_data()

    def bind_data(self):
        cbox = self.findChild(QtWidgets.QComboBox, 'connDriverComboBox')
        for i, label in enumerate(SQL_DRIVER_TO_LABEL.values()):
            cbox.insertItem(i, label)

    def accepted(self, *args, **kwargs):
        save_conn(
            self.get_qlineedit_text('connNameLineEdit'),
            self.get_qlineedit_text('connHostLineEdit'),
            self.get_qlineedit_text('connPortLineEdit'),
            self.get_qlineedit_text('connUsernameLineEdit'),
            self.get_qlineedit_text('connPasswordLineEdit'),
            self.get_qlineedit_text('connDatabaseNameLineEdit'),
            self.get_combobox_selected_text('connDriverComboBox'),
        )

# Misc
# ----------------------------------------------------------------------------

def get_dark_theme_palette():
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
    return palette

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setPalette(get_dark_theme_palette())
    try:
        main = MainWindow()
        main.show()
    except Exception as ex:
        print(ex)
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

