# -*- coding: utf-8 -*-
# @Time    : 2020 06/01
# @Author  : zhangpengjie
# @File    : AutoUpdate.py
# @Software: PyCharm
# @Function: 实现客户端自动更新（客户端）
import os
import sys
import time
import getopt
import requests
import tkinter
from tkinter import messagebox
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


# 处理xml的类
class VersionInfoXml:
    def __init__(self, xml_path, server_info=None, module_list=None):
        self.xml_path = xml_path
        if server_info is not None:
            if module_list is None:
                module_list = ["ClientVersion"]
            self.create_new_xml(server_info, module_list)
        self.tree = ET.parse(self.xml_path)
        self.root = self.tree.getroot()

    def create_new_xml(self, server_info, module_info):
        root = ET.Element("versionInfo")
        ServerInfo = ET.SubElement(root, "ServerInfo")
        ET.SubElement(ServerInfo, "ServerIp").text = server_info[0]
        ET.SubElement(ServerInfo, "ServerPort").text = server_info[1]
        ET.SubElement(ServerInfo, "XmlLocalPath").text = server_info[2]
        for each_module in module_info:
            ET.SubElement(root, each_module).set("Version", "0")
        self.save_change(root)
        print("I created a new temp xml!")

    def save_change(self, root=None):
        if root is None:
            root = self.root
        rough_bytes = ET.tostring(root, "utf-8")
        rough_string = str(rough_bytes, encoding="utf-8").replace("\n", "").replace("\t", "").replace("    ", "")
        content = minidom.parseString(rough_string)
        with open(self.xml_path, 'w+') as fs:
            content.writexml(fs, indent="", addindent="\t", newl="\n", encoding="utf-8")
        return True

    def changeServerInfo(self, name, value):
        if type(value) is int:
            value = str(value)
        Xpath = "ServerInfo/%s" % name
        element = self.root.find(Xpath)
        if element is not None:
            element.text = value
            # self.save_change()
        else:
            print("I can't find \"ServerInfo/%s\" in xml!" % name)

    def addObject(self, module_name, file_path, file_size, last_update_time, version):
        moduleVersion = self.root.find(module_name)
        object = ET.SubElement(moduleVersion, "object")
        ET.SubElement(object, "FileRelativePath").text = str(file_path)
        ET.SubElement(object, "FileSize").text = str(file_size)
        ET.SubElement(object, "LastUpdateTime").text = str(last_update_time)
        ET.SubElement(object, "Version").text = str(version)
        # self.save_change()

    def deleteObject(self, module_name, file_name):
        Xpath = "%s/object" % module_name
        objects = self.root.findall(Xpath)
        moudleVersion = self.root.find(module_name)
        for element in objects:
            if element.find('FileRelativePath').text == file_name:
                moudleVersion.remove(element)
                # self.save_change()
                print("Delete object: %s" % file_name)
                break
        else:
            print("I can't find \"%s\" in xml!" % file_name)

    def updateObject(self, module_name, file_name, version):
        if type(version) is int:
            version = str(version)
        Xpath = "%s/object" % module_name
        objects = self.root.findall(Xpath)
        for element in objects:
            if element.find('FileRelativePath').text == file_name:
                element.find('Version').text = version
                # self.save_change()
                # print("Update \"%s\" version: %s" % (file_name, version))
                break
        else:
            print("I can't find \"%s\" in xml!" % file_name)

    def getObjects(self, module_name):
        list_element = []
        Xpath = "%s/object" % module_name
        objects = self.root.findall(Xpath)
        for element in objects:
            dict_element = {}
            for key, value in enumerate(element):
                dict_element[value.tag] = value.text
            list_element.append(dict_element)
        return list_element

    def getModules(self):
        dict_element = {}
        objects = self.root.getchildren()
        for key, value in enumerate(objects):
            dict_element[value.tag] = value.attrib.get("Version")
        del dict_element["ServerInfo"]
        return dict_element

    def addModule(self, module):
        self.root.append(module)
        # self.save_change()

    def deleteModule(self, module_name):
        module = self.root.find(module_name)
        if module is not None:
            self.root.remove(module)
            # self.save_change()

    def getAttribute(self, module_name):
        moduleVersion = self.root.find(module_name)
        if moduleVersion is None:
            return None
        return moduleVersion.get("Version")

    def updateAttribute(self, module_name, version):
        if type(version) is int:
            version = str(version)
        moduleVersion = self.root.find(module_name)
        moduleVersion.set("Version", version)
        # self.save_change()

    def get_node_value(self, path):
        """
        查找某个路径匹配的第一个节点
        tree: xml树
        path: 节点路径
        """
        node = self.tree.find(path)
        if node == None:
            return None
        return node.text
  
# 手动更新时，检查更新
def CheckUpdate(server_ip, server_port, module_name, order):
    update_flag = tkinter.messagebox.askokcancel('客户端自动升级检测', '检测到客户端更新，是否立即开始更新？')
    print(update_flag)
    print(server_ip, server_port, module_name, order)
    if update_flag == True:
        flag = AutoUpdate(server_ip, server_port, module_name, order)
        return flag
    else:
        return False


# 主要函数
def AutoUpdate(server_ip, server_port, module_name, order):
    time_start = time.perf_counter()
    try:
        download_url = "http://{0}:{1}/{2}".format(server_ip,server_port, "VersionInfo.xml")
        # 由于云平台端口映射的问题，需要用域名方式访问
        # download_url = "http://{0}/ClientFolder/{1}".format(server_ip, each_file)
        # local_path = os.path.join(sys.path[0], "VersionInfoTemp.xml")
        local_path = "./VersionInfoTemp.xml"
        print("download_url: " + download_url)
        if not download_file_by_http(download_url, local_path):
            raise Exception()
    except Exception as e:
        # tkinter.messagebox.showerror("更新无法继续", "获取最新版本列表文件出现异常！")
        print("Update error: Can't get the latest VersionInfo xml!")
        # root.destroy()
        return False
    # root.update()
    # root.deiconify()
    # 比较文件变化
    add_dict, delete_list = analyze_update_info(local_xml_path, update_xml_path, module_name)
    #barometer只需判断是否需要更新，无需更新xml
    if add_dict == {} and delete_list == []:
        os.remove(update_xml_path)
        # tkinter.messagebox.showinfo("更新无法继续", "当前客户端已经是最新版本！")
        print("No file changed!")
        return False
    else:
        os.remove(update_xml_path)#remove temp_xml
        return True
    '''
    if add_dict == {} and delete_list == []:
        os.remove(update_xml_path)
        # tkinter.messagebox.showinfo("更新无法继续", "当前客户端已经是最新版本！")
        print("No file changed!")
        return False
    else:
        if module_name == "all_module":
            os.remove(local_xml_path)
            os.rename(update_xml_path, local_xml_path)
        else:
            update_xml(local_xml_path, update_xml_path, module_name)
        return True
    '''

# 分析两个xml文件
def analyze_update_info(local_xml, update_xml, module_name):
    '''
    分析本地xml文件和最新xml文件获得增加的文件和要删除的文件
    :param local_xml: 本地xml文件路径
    :param update_xml: 下载的最新xml文件路径
    :return: download_info: {filename1: fizesize1, filename2: fizesize2}, delete_list: [filname1, filname2]
    '''
    print("Analyze the xml files and check the version number ...")
    old_xml = VersionInfoXml(local_xml)
    new_xml = VersionInfoXml(update_xml)
    module_names = []
    if module_name == "all_module":
        module_names = new_xml.getModules()
    else:
        module_names.append(module_name)
    download_info_total = {}
    delete_list_total = []
    for module_name in module_names:
        if old_xml.getAttribute(module_name) is None:
            ET.SubElement(old_xml.root, module_name).set("Version", "0")
        if new_xml.getAttribute(module_name) <= old_xml.getAttribute(module_name):
            continue
        old_xml_objects = old_xml.getObjects(module_name)
        new_xml_objects = new_xml.getObjects(module_name)
        old_xml_objects_dict = {file_info["FileRelativePath"]: file_info for file_info in old_xml_objects}
        new_xml_objects_dict = {file_info["FileRelativePath"]: file_info for file_info in new_xml_objects}
        old_data_list = set(old_xml_objects_dict.keys())
        new_data_list = set(new_xml_objects_dict.keys())
        add_list = list(new_data_list.difference(old_data_list))
        delete_list = list(old_data_list.difference(new_data_list))
        common_list = list(old_data_list.intersection(new_data_list))

        download_info = {file_name: new_xml_objects_dict[file_name]["FileSize"] for file_name in add_list}
        # 根据每个文件的版本号，确定是否需要更新
        for file_name in common_list:
            if int(new_xml_objects_dict[file_name]["Version"]) > int(old_xml_objects_dict[file_name]["Version"]):
                download_info.update({file_name: new_xml_objects_dict[file_name]["FileSize"]})

        download_info_total.update(download_info)
        delete_list_total.extend(delete_list)
    # return download_info, delete_list
    return download_info_total, delete_list_total


# 下载
def download_file_by_http(down_load_url, dest_file_path):
    r = requests.get(down_load_url, timeout=10, params=None)
    print(r.status_code)
    try:
        with open(dest_file_path, "wb") as code:
            code.write(r.content)
        if r.status_code == 200:
            ret = True
        else:
            ret = False
        r.close()
        return ret
    except:
        r.close()
        return False


# 更新xml文件
def update_xml(local_xml_path, update_xml_path, module_name):
    old_xml = VersionInfoXml(local_xml_path)
    new_xml = VersionInfoXml(update_xml_path)
    new_server_module = new_xml.root.find("ServerInfo")
    new_module = new_xml.root.find(module_name)
    old_xml.deleteModule("ServerInfo")
    old_xml.addModule(new_server_module)
    old_xml.deleteModule(module_name)
    old_xml.addModule(new_module)
    old_xml.save_change()
    os.remove(update_xml_path)


# region 获取并处理命令行参数
module_name = "ClientVersion"
order = "update"
client_pid = 0  # 旧客户端进程pid，更新主客户端时用于重启
try:
    opts, args = getopt.getopt(sys.argv[1:], "c:p:o:")
except getopt.GetoptError:
    print('test.py -c <module_name> -p<pid> -o<add,delete,update>')
    sys.exit(2)
for opt, value in opts:
    if opt == "-c":
        module_name = value
    elif opt == "-p":
        client_pid = value
    elif opt == "-o":
        order = value
# endregion

# 启动窗口
# local_xml_path = os.path.join(sys.path[0], "VersionInfo.xml")
local_xml_path = "./VersionInfo.xml"
# update_xml_path = os.path.join(sys.path[0], "VersionInfoTemp.xml")
update_xml_path = "./VersionInfoTemp.xml"
local_xml = VersionInfoXml(local_xml_path)
server_ip = local_xml.get_node_value("ServerInfo/ServerIp")
server_port = local_xml.get_node_value("ServerInfo/ServerPort")
del local_xml


def updateJudge():
    update_flag = AutoUpdate(server_ip, server_port, module_name, order)
    return update_flag
