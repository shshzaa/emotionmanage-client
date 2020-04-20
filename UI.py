# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1500, 800)
        label_Title = QtWidgets.QLabel(self)
        # self.layoutTitle.addWidget(label_Title,QtCore.Qt.AlignCenter)
        label_Title.setText('自我关爱，从微记录开始')
        label_Title.setFixedWidth(1500)
        label_Title.setFixedHeight(180)
        label_Title.setAlignment(QtCore.Qt.AlignCenter)
        label_Title.setFont(QtGui.QFont("华文行楷",24,QtGui.QFont.Bold))


        self.layoutWidget = QtWidgets.QWidget(Dialog)
        # self.layoutWidget.setGeometry(QtCore.QRect(220, 270, 500, 200))
        self.layoutWidget.setObjectName("layoutWidget")
        # self.verticalLayout1 = QtWidgets.QVBoxLayout(self.layoutWidget)
        # self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        # self.horizontalLayout.setContentsMargins(600,200,0,0)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        # self.verticalLayout.setAlignment()
        # self.verticalLayout.addWidget(label_Title,0,QtCore.Qt.AlignCenter)
        self.verticalLayout.setContentsMargins(350, 250, 0, 0)


        self.pushButton_info = QtWidgets.QPushButton(Dialog)
        self.pushButton_info.setObjectName('pushButton_info')
        self.pushButton_info.setGeometry(QtCore.QRect(440, 560, 180, 50))
        self.pushButton_info.setStyleSheet("#pushButton_info{backgroud:white;border:2px solid gray;border-radius:10px;}")
        self.pushButton_info.setText("查看个人信息")
        self.pushButton_info.setFont(QtGui.QFont("宋体", 12))
        self.pushButton_submit = QtWidgets.QPushButton(Dialog)
        self.pushButton_submit.setObjectName('pushButton_submit')
        self.pushButton_submit.setGeometry(QtCore.QRect(840, 560, 180, 50))
        self.pushButton_submit.setText("提交")
        self.pushButton_submit.setFont(QtGui.QFont("宋体", 12))
        self.pushButton_submit.setStyleSheet("#pushButton_submit{backgroud:white;border:2px solid gray;border-radius:10px;}")
        # self.pushButton_submit.setStyleSheet("border-color: rgb(170, 150, 163);")



