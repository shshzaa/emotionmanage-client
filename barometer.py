# -*- coding: utf-8 -*-

import json
import  PyQt5.QtWebEngineWidgets
from PyQt5 import QtCore,QtWidgets,QtGui
from UI import Ui_Dialog
import os
# from tkinter import *
import tkinter
from tkinter import ttk
import client
from PIL import ImageTk,Image
import socket
from psutil import net_if_addrs
import requests
import logging
import subprocess


# server_url = 'http://emotion.test.cloud.zj.sgcc.com.cn'#服务器地址
server_url = 'http://www.baidu.com'#服务器地址


class Barometer(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self,parent=None):
       super(Barometer, self).__init__(parent)
       self.userposition = ''
       self.usergender = ''
       self.usercompany = ''
       self.userdepartment = ''
       self.hostname = ''
       self.username = ''
       self.userid = ''
       self.usergroup = ''
       self.ip = ''
       self.mac = ''
       self.windowTitle = "自我关爱，从微记录开始"
       self.tktitle = '首次登陆'
       self.departmentFlag = False
       self.existCount = 0
       # self.setupUi(self)
       self.initUI()

    def logger(self):

        logging.basicConfig(level=logging.INFO,
                            filename='./log.txt',
                            filemode='a',
                            format='%(asctime)s:%(message)s')
        # use logging
        logging.info('success')
        
    def initUI(self):
        updateflag = client.updateJudge()
        print(updateflag)
        if updateflag:
            bat = open('upgrade.bat','w')
            TempList = "@echo off\n"
            TempList += "start " + os.path.dirname(sys.path[0]) + '\\update\\update.exe'
            print(TempList)
            bat.write(TempList)
            bat.close()
            subprocess.Popen("upgrade.bat")
            sys.exit()
        self.get_ip_address()
        self.get_mac_address()
        if not os.path.exists('config.json'):
            self.login_template()
        # self.get_info_from_config()

        # self.pushButton_info.clicked.connect(self.info)
        # self.pushButton_submit.clicked.connect(self.submit)
        # self.showQuestionare()
        print('mac='+self.mac)
        # self.welcome()
        self.showMainInterface()

    def appExit(self):

        if(self.browser.title() =='exit'):
            self.logger()
            sys.exit(app.exec())

    def showMainInterface(self):
        # url_display = server_url
        # C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup
        url_display = server_url + '/client?MacAddress='+self.mac
        # url_display = 'http://www.runoob.com/ajax/ajax-example.html'
        self.browser = WebEngineView()
        self.browser.load(QtCore.QUrl(url_display))
        self.browser.setFont(QtGui.QFont("宋体", 10, QtGui.QFont.Bold))
        self.browser.setWindowTitle('心情晴雨表')
        self.browser.setWindowOpacity(0.95)

        self.browser.resize(1150, 600)
        self.browser.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.browser.titleChanged.connect(self.appExit)
        self.browser.show()


        print("info")


    def welcome(self):
        print('wel')
        self.tktitle = '修改个人信息'
        label_welcome = myLabel(self)
        label_welcome.setText('你好，' + self.username)
        label_welcome.setFont(QtGui.QFont("宋体", 12, QtGui.QFont.Bold))
        label_welcome.setGeometry(QtCore.QRect(1000, 160, 400, 50))
        label_welcome.clicked.connect(self.login_template)
        # self.clicked.connect(self.personalInfo_change)

    def login_template(self):
        print('修改个人信息')
        tip = '心理学研究表明，关注自我情绪状况，做好自我情绪管理，是保持心理健康的重要途径。' \
              '公司开发了“心情晴雨表”小工具，帮助您梳理和记录日常点滴。' \
              '基本信息仅需填写一次，填答要每天坚持哦，心理关爱，自己做起～'
        root = tkinter.Tk()
        root.title(self.tktitle)
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (1280, 720, (screenwidth - 1280) / 2, (screenheight - 720) / 2)  # 屏幕居中显示
        root.geometry(size)
        if self.tktitle == '首次登陆':
            root.overrideredirect(True)
        canvas = tkinter.Canvas(root,width=1280,height= 720,bd=10,highlightthickness=1)
        img = Image.open('loginfirst.png')
        photo = ImageTk.PhotoImage(img)
        canvas.create_image(0,0,anchor = tkinter.NW,image=photo)
        for i in range(0,len(tip),15):
            canvas.create_text(1030,220+i*2, text=tip[i:i+15],font =("华文行楷",12))
        canvas.pack()

        canvas.create_text(640, 70, text=self.tktitle, font=("华文行楷", 24))
        # 姓名
        tkinter.Label(root, text="姓名：",font=('宋体',12)).place(x= 20,y=150)

        name_text = tkinter.StringVar()
        name = tkinter.Entry(root, textvariable=name_text)
        if self.tktitle == '首次登陆':
            name_text.set("")
        else:
            name_text.set(self.username)
        name.place(x=100,y=150)
        #工号
        tkinter.Label(root, text="工号：",font=('宋体',12)).place(x= 380,y=150)
        id_text = tkinter.StringVar()
        id = tkinter.Entry(root, textvariable=id_text)
        if self.tktitle == '首次登陆':
            id_text.set("")
        else:
            id_text.set(self.userid)
        id.place(x=460,y=150)
        # 性别
        def gender(event):
            self.usergender = comboxlist_gender.get()
            print(self.usergender)

        tkinter.Label(root, text="性别：",font=('宋体',12)).place(x=20,y=250)
        comvalue_gender = tkinter.StringVar()
        comboxlist_gender = ttk.Combobox(root, textvariable=comvalue_gender)  # 初始化
        comboxlist_gender["values"] = ("男","女")
        # comboxlist_gender.current(0)  # 选择第一个
        comboxlist_gender.bind("<<ComboboxSelected>>", gender)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
        comboxlist_gender.place(x=100,y=250)
        # 职位
        def position(event):
            self.userposition = positionlist.index(comboxlist_position.get()) + 1
            print(self.userposition)


        tkinter.Label(root, text="职位：",font=('宋体',12)).place(x=380, y = 250)
        comvalue_position = tkinter.StringVar()
        comboxlist_position = ttk.Combobox(root, textvariable=comvalue_position)  # 初始化
        positionlist = ["普通员工","班组长&副班组长","主任&副主任","公司领导","省公司党建"]
        comboxlist_position["values"] = positionlist
        # comboxlist_position.current(4)  # 选择第一个
        comboxlist_position.bind("<<ComboboxSelected>>", position)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
        comboxlist_position.place(x=460,y=250)
        # 公司
        def company(event):
            self.usercompany = comboxlist_company.get()
            print(self.usercompany)
            CompanyId = list (company_data_json.keys()) [list (company_data_json.values()).index (comboxlist_company.get())]
            if self.userposition != 4 and self.userposition != 5 :
                url_getdepartment = server_url + '/getdepartment' + '?CompanyId=' + CompanyId
                print(url_getdepartment)
                req = requests.get(url=url_getdepartment)
                department_data = req.content.decode()
                department_data_trans = department_data.encode('utf-8').decode('unicode_escape')
                self.department_data_json = json.loads(department_data_trans)
                departmentlist = []
                # departmentlist = ['11','12']
                for value in self.department_data_json.values(): departmentlist.append(value)
                comboxlist_department["values"] = departmentlist
                userdepart.place(x=380,y=350)
                comboxlist_department.place(x=460,y=350)
            else:
                userdepart.place_forget()
                comboxlist_department.place_forget()
                usergroup.place_forget()
                comboxlist_group.place_forget()

        url_getcompany = server_url + '/getcompany'
        print(url_getcompany)
        req = requests.get(url=url_getcompany)
        print(req)
        company_data = req.content.decode()

        company_data_trans = company_data.encode('utf-8').decode('unicode_escape')
        print(company_data_trans)
        company_data_json = json.loads(company_data_trans)
        print(company_data_json)
        tkinter.Label(root, text="公司：",font=('宋体',12)).place(x=20,y=350)
        comvalue_company = tkinter.StringVar()
        comboxlist_company = ttk.Combobox(root, textvariable=comvalue_company)
        companylist= []
        for value in company_data_json.values():companylist.append(value)# 初始化
        comboxlist_company["values"] = companylist
        comboxlist_company.bind("<<ComboboxSelected>>", company)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
        comboxlist_company.place(x=100,y=350)

        # 部门
        def department(event):
            self.userdepartment  = comboxlist_department.get()
            print(self.userdepartment)
            DepartmentId = list (self.department_data_json.keys()) [list (self.department_data_json.values()).index (comboxlist_department.get())]
            if self.userposition == 1 or self.userposition == 2:
                url_getgroup = server_url + '/getgroupset' + "?DepartmentId=" + DepartmentId
                print(url_getgroup)
                req = requests.get(url=url_getgroup)
                group_data = req.content.decode()
                group_data_trans = group_data.encode('utf-8').decode('unicode_escape')
                self.group_data_json = json.loads(group_data_trans)
                grouplist = []
                # grouplist = ['123','1234']
                for value in self.group_data_json.values(): grouplist.append(value)
                comboxlist_group["values"] = grouplist
                usergroup.place(x=20,y=450)
                comboxlist_group.place(x=100,y=450)

            else:
                usergroup.place_forget()
                comboxlist_group.place_forget()


        userdepart = tkinter.Label(root, text="部门：",font=('宋体',12))
        comvalue_department = tkinter.StringVar()
        comboxlist_department = ttk.Combobox(root, textvariable=comvalue_department)  # 初始化
        comboxlist_department.bind("<<ComboboxSelected>>", department)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)

        # 班组
        def group(event):
            print('group')
            self.usergroup = comboxlist_group.get()
            print(self.usergroup)


        usergroup = tkinter.Label(root, text="班组：",font=('宋体',12))
        comvalue_group = tkinter.StringVar()
        comboxlist_group = ttk.Combobox(root, textvariable=comvalue_group)  # 初始化
        comboxlist_group.bind("<<ComboboxSelected>>", group)

        # 按钮
        def on_click():
            if name_text.get() == '' or id_text.get() == '':
                msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.NoIcon, '温馨提醒', "还有没有选的，快去完成吧！")
                msg.setIconPixmap(QtGui.QPixmap('logo.jpg'))
                msg.exec()
            else:
                fp = open('config.json', 'w')
                self.username = name_text.get()
                self.userid = id_text.get()
                Userinfo = {}
                Userinfo['username'] = self.username
                Userinfo['userid'] = self.userid
                Userinfo['ip'] = self.ip
                Userinfo['mac'] = self.mac
                Userinfo['company'] = self.usercompany
                Userinfo['department'] = self.userdepartment
                Userinfo['groupset'] = self.usergroup
                Userinfo['position'] = self.userposition
                Userinfo['gender'] = self.usergender
                Username_str = json.dumps(Userinfo)
                fp.write(Username_str)

                data = {}
                data['Id'] = self.userid
                data['MacAddress'] = self.mac
                data['Name'] = self.username
                data['Company'] = self.usercompany
                data['Department'] = self.userdepartment
                data['GroupSet'] = self.usergroup
                data['Position'] = self.userposition
                data['Gender'] = self.usergender
                json_data = json.dumps(data)
                print(data)
                if self.tktitle == '首次登陆':
                    url_login = server_url + '/regist'
                else:
                    url_login = server_url + '/modify'
                req = requests.post(url=url_login, data=json_data)
                print(req.content.decode())
                root.quit()
                root.destroy()
        tkinter.Button(root, text='确定', command=on_click, width=15).place(x=550,y =450)
        root.mainloop()


    def showQuestionare(self):
        self.setWindowTitle(self.windowTitle)
        for i in range(self.questionarenum):
            label = QtWidgets.QLabel(self)
            label.setText(str(i+1)+"."+self.question[i])
            label.setFont(QtGui.QFont("华文行楷",16))
            self.verticalLayout.addWidget(label)
            self.verticalLayout.setSpacing(20)
            self.layout = QtWidgets.QHBoxLayout()

            self.verticalLayout.addLayout(self.layout)
            buttonGroup = QtWidgets.QButtonGroup(self)
            # buttonGroup.setObjectName(str(i))
            for answer in self.questionare[self.question[i]]:
                id = str(i) + '-' + str(self.questionare[self.question[i]].index(answer)+1)
                radioButton = QtWidgets.QRadioButton(answer,self)
                radioButton.setObjectName(id)
                radioButton.setFont(QtGui.QFont("宋体", 12))
                buttonGroup.addButton(radioButton)
                radioButton.clicked.connect(self.radioButtonState)
                self.layout.addWidget(radioButton)

    def radioButtonState(self):
        sender = self.sender()
        clickedId = sender.objectName()
        questionId = int(clickedId.split('-')[0])
        answerId = int(clickedId.split('-')[1])
        self.result[questionId] = answerId
        self.data[str(questionId+1)] = answerId

    def get_mac_address(self):
        for k, v in net_if_addrs().items():
            mac_temp = ''
            for item in v:
                address = item[1]
                if '-' in address and len(address) == 17:
                    mac_temp = address
                if address == self.ip:
                    self.mac = mac_temp
                    print(self.mac)


    def get_ip_address(self):
        hostname_socket = socket.gethostname()
        self.hostname = hostname_socket
        print(self.hostname)
        #获取本机ip,通过socket连接获取本机ip，解决了原socket.gethostbyname()方法不支持中文主机名的问题
        try:
            
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            s.connect(('127.0.0.1', 80))
            
            print(s.getsockname())
            self.ip = s.getsockname()[0]
        finally:
            print('iperror')
            s.close()
        # 获取本机ip,只支持英文名主机，socket包的问题
        # self.ip = socket.gethostbyname(hostname_socket)
        print('ip')
        print(self.ip)


    def get_info_from_config(self):
        with open("config.json",'r') as load_f:
            load_dict = json.load(load_f)
            print(load_dict)
            self.username = load_dict['username']
            self.userid = load_dict['userid']
            self.ip = load_dict['ip']
            self.mac = load_dict['mac']

    def submit(self):
        if 0 in self.result:
            # QtWidgets.QMessageBox.information(self,'温馨提醒','还有没有选的，快去完成吧！')
            msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.NoIcon, '温馨提醒', "还有没有选的，快去完成吧！")
            msg.setIconPixmap(QtGui.QPixmap('logo.jpg'))
            msg.exec()
        else:
            self.data['MacAddress'] = self.mac
            data = json.dumps(self.data)
            print(self.data)
            url_upload = server_url + '/upload'
            req = requests.post(url = url_upload,data = data)
            # msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.NoIcon, req.content.decode())
            tips = req.content.decode()
            # tips = '心理学研究表明，关注自我情绪状况，做好自我情绪管理，是保持心理健康的重要途径。' \
            #       '公司开发了“心情晴雨表”小工具，帮助您梳理和记录日常点滴。' \
            #       '基本信息仅需填写一次，填答要每天坚持哦，心理关爱，自己做起～'
            root = tkinter.Tk()
            screenwidth = root.winfo_screenwidth()
            screenheight = root.winfo_screenheight()
            size = '%dx%d+%d+%d' % (800, 800, (screenwidth - 800) / 2, (screenheight - 800) / 2)  # 屏幕居中显示
            root.geometry(size)
            root.overrideredirect(True)
            canvas = tkinter.Canvas(root, width=800, height=800, bd=0, highlightthickness=1)
            img = Image.open('tip.png')
            photo = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
            for i in range(0, len(tips), 15):
                print(i)
                canvas.create_text(400, 250 + i * 3, text=tips[i:i + 15], font=("宋体", 12))
            canvas.pack()

            def on_click():
                root.quit()
                root.destroy()

            tkinter.Button(root, text='确定', command=on_click, width=15).place(x=500, y=700)
            root.mainloop()
            # msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.NoIcon, '生活小贴士', "感谢您的使用!")
            # msg_box.setIconPixmap(QtGui.QPixmap('logo.jpg'))
            # msg_box.exec()
            #使用时需开启
            self.logger()

            print('提交成功')

            sys.exit(app.exec())





class WebEngineView(PyQt5.QtWebEngineWidgets.QWebEngineView):
    windowList = []

    # 重写createwindow()
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview =   WebEngineView()
        new_window = QtWidgets.QMainWindow()
        new_window.setCentralWidget(new_webview)
        #new_window.show()
        self.windowList.append(new_window)  #注：没有这句会崩溃！！！
        return new_webview

class myLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()

if __name__ == '__main__':
    import sys
    app =   QtWidgets.QApplication(sys.argv)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseSoftwareOpenGL)#openGL
    main = QtWidgets.QMainWindow()
    try:
        code = requests.get(server_url).status_code
    except:
        print("Internet error")
        sys.exit()
    else:
        if(code  != 200):
            print("server failure")
            sys.exit()
        else:
            screen = Barometer()
            # screen.setObjectName('screen')
            # screen.setWindowOpacity(0.95)
            # screen.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            # screen.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            # screen.setStyleSheet("#screen{border-image:url(./bg1400x800.jpg);border: 20px soild white;border-radius:50px;}")
            # screen.setWindowIcon(QtGui.QIcon('./icon_32.ico'))
            # screen.show()
            sys.exit(app.exec_())
 