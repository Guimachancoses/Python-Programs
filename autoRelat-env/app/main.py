from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QDate
from PyQt5.QtPrintSupport import *
from paineRelat import Ui_Extract
import os,sys

class login(QDialog):
    def __init__(self, *args, **argvs):
        super (login,self).__init__(*args,**argvs)
        self.ui = Ui_Extract()
        self.ui.setupUi(self)
        self.ui.checkBox.clicked.connect(self.toggle_checkboxes)
        self.ui.download.clicked.connect(self.retrieve_dates)
        self.ui.download.clicked.connect(self.retrieve_selected_radios)

    def toggle_checkboxes(self):
        all_radios = [
            self.ui.paulina, 
            self.ui.bauru, 
            self.ui.saoPaulo, 
            self.ui.barueri, 
            self.ui.canoas, 
            self.ui.passoFundo,
            self.ui.rioGrande,
            self.ui.campoGrande,
            self.ui.presPrudente,
            self.ui.araucaria,
            self.ui.cascavel,
            self.ui.guarapuava,
            self.ui.ijui,
            self.ui.chapeco,
            self.ui.sms,
            self.ui.uberaba,
            self.ui.uberlandia,
            self.ui.goiania,
            self.ui.lages,
            self.ui.brasilia,
            self.ui.sjc,
            self.ui.ribeiraoPreto,
            self.ui.itaituba1,
            self.ui.itaituba2,
            self.ui.cubatao,
            self.ui.itajai,
            self.ui.londrina,
            self.ui.maringa,
            self.ui.sjrp
        ]

        check_state = self.ui.checkBox.isChecked()

        for radio_button in all_radios:
            radio_button.setChecked(check_state)
    
    def retrieve_dates(self):
        checkin_date = self.ui.checkin.date()
        checkout_date = self.ui.checkout.date()

        print("Checkin Date:", checkin_date.toString(Qt.ISODate))
        print("Checkout Date:", checkout_date.toString(Qt.ISODate))
    
    def retrieve_selected_radios(self):
        all_radios = [
            self.ui.paulina, 
            self.ui.bauru, 
            self.ui.saoPaulo, 
            self.ui.barueri, 
            self.ui.canoas, 
            self.ui.passoFundo,
            self.ui.rioGrande,
            self.ui.campoGrande,
            self.ui.presPrudente,
            self.ui.araucaria,
            self.ui.cascavel,
            self.ui.guarapuava,
            self.ui.ijui,
            self.ui.chapeco,
            self.ui.sms,
            self.ui.uberaba,
            self.ui.uberlandia,
            self.ui.goiania,
            self.ui.lages,
            self.ui.brasilia,
            self.ui.sjc,
            self.ui.ribeiraoPreto,
            self.ui.itaituba1,
            self.ui.itaituba2,
            self.ui.cubatao,
            self.ui.itajai,
            self.ui.londrina,
            self.ui.maringa,
            self.ui.sjrp
        ]

        for radio_button in all_radios:
            if radio_button.isChecked():
                print("Selected:", radio_button.text())


app = QApplication(sys.argv)
if (QDialog.Accepted == True):
    window = login()
    window.show()
sys.exit(app.exec_())

