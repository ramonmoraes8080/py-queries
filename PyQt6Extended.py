from PyQt6 import (
    QtWidgets,
    uic,
)


class QWidgetFromTemplate(object):

    template_path = None

    def __init__(self, *args, **kwargs):
        if not self.template_path:
            raise Exception("template_path cannot be None")
        uic.loadUi(self.template_path, self)
        self.bind_data()

    def bind_data(self):
        pass


class QWidgetUtilities(object):

    def get_qlineedit_text(self, obj_name):
        return self.findChild(QtWidgets.QLineEdit, obj_name).text()

    def get_combobox_selected_text(self, obj_name):
        combobox = self.findChild(QtWidgets.QComboBox, obj_name)
        return combobox.itemText(combobox.currentIndex())

    def get_qplaintextedit_text(self, obj_name):
        qplaintextedit = self.findChild(QtWidgets.QPlainTextEdit, obj_name)
        return qplaintextedit.toPlainText()

    def get_qtabwidget(self, obj_name):
        return self.findChild(QtWidgets.QTabWidget, obj_name)

    def get_qtablewidget(self, obj_name):
        return self.findChild(QtWidgets.QTableWidget, obj_name)

    def get_plaintextedit(self, obj_name):
        return self.findChild(QtWidgets.QPlainTextEdit, obj_name)

    def get_textedit(self, obj_name):
        return self.findChild(QtWidgets.QTextEdit, obj_name)

    def get_tab(self, obj_name):
        return self.findChild(QtWidgets.QTabWidget, obj_name)


class QMainWindowExtended(QtWidgets.QMainWindow, QWidgetFromTemplate, QWidgetUtilities):
    pass


class QWidgetExtended(QtWidgets.QWidget, QWidgetFromTemplate, QWidgetUtilities):
    pass


class QDialogExtended(QtWidgets.QDialog, QWidgetFromTemplate, QWidgetUtilities):
    pass

