import os, sys
import os.path
import jinja2

from jinja2 import Template

import numpy as np
from numpy import genfromtxt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import QFileInfo
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from pathlib import Path

# UI
class Ui_MainWindow(object):
    # load csv file
    def browse_button(self):
        global filename
        filename = str(QtWidgets.QFileDialog.getOpenFileName(None, "Open Data File", ""))
        # self.label_3.setText(filename)
        dir = Path(filename).stem
        dir = dir + ".csv"
        global my_data
        with open(dir, 'r') as csvfile:
            # creating a csv reader object
            my_data = genfromtxt(dir, delimiter=',', dtype=float)

    # funkce ulozeni souboru
    def save_button(self):
        global dir_name
        dir_name = QtWidgets.QFileDialog.getExistingDirectory()
        # self.label_5.setText(dir_name)

    # quit
    def quit(self):
        MainWindow.close()

    # main function
    def DoTheJob(self):
        # each calculation
        a = my_data[1:, 1]
        b = my_data[1:, 2]
        c = my_data[1:, 3]
        d = my_data[1:, 4]
        v = my_data[1:, 5]
        amean = np.mean(a)
        bmean = np.mean(b)
        cmean = np.mean(c)
        dmean = np.mean(d)
        vmean = np.mean(v)
        num_rows = np.size(my_data, 0)
        num_rows = num_rows - 1
        nejistotaa = 1 / (num_rows * (num_rows - 1))

        aneja = np.sqrt(nejistotaa * np.square(np.sum(a - amean)))
        bneja = np.sqrt(nejistotaa * np.square(np.sum(b - bmean)))
        cneja = np.sqrt(nejistotaa * np.square(np.sum(c - cmean)))
        dneja = np.sqrt(nejistotaa * np.square(np.sum(d - dmean)))
        vneja = np.sqrt(nejistotaa * np.square(np.sum(v - vmean)))

        osobchyb = 0.5 / np.sqrt(3)
        prist1chyba = 0.5 / np.sqrt(3)
        prist2chyba = 0.1 / np.sqrt(3)

        kombchyba = np.sqrt(np.square(aneja) + np.square(prist1chyba))
        kombchybb = np.sqrt(np.square(bneja) + np.square(prist2chyba))
        kombchybc = np.sqrt(np.square(cneja) + np.square(prist2chyba))
        kombchybd = np.sqrt(np.square(dneja) + np.square(prist1chyba))
        kombchybv = np.sqrt(np.square(vneja) + np.square(prist2chyba))

        # konecna slozka
        filename = foldname + ".tex"
        save_file = os.path.join(dir_name, filename)

        # template
        latex_jinja_env = jinja2.Environment(
            block_start_string='\BLOCK{',
            block_end_string='}',
            variable_start_string='\VAR{',
            variable_end_string='}',
            comment_start_string='\#{',
            comment_end_string='}',
            line_statement_prefix='%%',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
            loader=jinja2.FileSystemLoader(os.path.abspath('.'))
        )
        template = latex_jinja_env.get_template('template.tex')
        report = template.render(stroj1='Osobni chyba', chyba1=chyba3, stroj2=pristroj1,
                                 chyba2=chyba1, stroj3=pristroj2, chyba3=chyba2,
                                 table1=my_data, vys1=kombchyba, vys2=kombchybb, vys3=kombchybc,
                                 vys4=kombchybd, vys5=kombchybv)
        with open(save_file, "w") as output:
            output.write(report)

        """
        # Email
        fromaddr = "projektyvscht@gmail.com"
        frompass = "projektS1"
        toaddr = mail

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = 'Your report'
        body = "Your generated report"

        msg.attach(MIMEText(body, 'plain'))

        mailfile = save_file

        pdf = MIMEApplication(open(mailfile, 'rb').read())
        pdf.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(pdf)

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtpObj:
                smtpObj.ehlo()
                smtpObj.starttls()
                smtpObj.login(fromaddr, frompass)
                smtpObj.sendmail(fromaddr, toaddr, msg.as_string())
        except Exception as e:
            print(e) 

        session = ftplib.FTP('ftp.byethost32.com', 'b32_28065368', 'projektyvscht456')
        file = open(save_file, 'rb')  # file to send
        session.cwd('htdocs')
        session.storbinary('STOR ' + filename, file)  # send the file
        file.close()  # close file and FTP
        session.quit()
    """

    def setupUi(self, MainWindow):
        global pristroj1
        global chyba1
        global pristroj2
        global chyba2
        global chyba3
        global foldname
        global mail
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(820, 749)
        self.onlyFloat = QDoubleValidator()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(530, 610, 101, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(quit)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(170, 610, 101, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.DoTheJob)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(640, 150, 101, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.browse_button)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(220, -10, 511, 131))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(270, 90, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 150, 601, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)

        self.label_3.setObjectName("label_3")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(640, 530, 101, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.save_button)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 530, 601, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 380, 201, 31))
        self.label_6.setObjectName("label_6")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(240, 380, 141, 31))
        self.lineEdit.setObjectName("lineEdit")
        foldname = self.lineEdit.text()
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(10, 450, 201, 31))
        self.label_7.setObjectName("label_7")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(240, 450, 141, 31))

        self.lineEdit_2.setObjectName("lineEdit_2")
        mail = self.lineEdit_2.text()
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(10, 320, 201, 31))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(10, 270, 201, 31))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(10, 220, 201, 31))
        self.label_10.setObjectName("label_10")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(240, 320, 141, 31))

        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setValidator(self.onlyFloat)
        chyba3 = self.lineEdit_3.text()
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(240, 270, 141, 31))

        self.lineEdit_4.setObjectName("lineEdit_4")
        pristroj2 = self.lineEdit_4.text()
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(460, 270, 141, 31))

        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_5.setValidator(self.onlyFloat)
        chyba2 = self.lineEdit_5.text()
        self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6.setGeometry(QtCore.QRect(240, 220, 141, 31))

        self.lineEdit_6.setObjectName("lineEdit_6")
        pristroj1 = self.lineEdit_6.text()
        self.lineEdit_7 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_7.setGeometry(QtCore.QRect(460, 220, 141, 31))

        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_7.setValidator(self.onlyFloat)
        chyba1 = self.lineEdit_7.text()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Storno"))
        self.pushButton_2.setText(_translate("MainWindow", "Proceed"))
        self.pushButton_3.setText(_translate("MainWindow", "Choose file"))
        self.label.setText(_translate("MainWindow", "This is automated report system"))
        self.label_2.setText(_translate("MainWindow", "Please select file with your data"))
        self.pushButton_4.setText(_translate("MainWindow", "Save file"))
        self.label_6.setText(_translate("MainWindow", "Name of PDF file (without.pdf)"))
        self.lineEdit.setText(_translate("MainWindow", "report"))
        self.label_7.setText(_translate("MainWindow", "Your e-mail adress"))
        self.label_8.setText(_translate("MainWindow", "Osobni chyba"))
        self.label_9.setText(_translate("MainWindow", "Pristroj 2 s chybou"))
        self.label_10.setText(_translate("MainWindow", "Pristroj 1 s chybou"))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
