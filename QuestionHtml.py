#
# class QuestionHtml():
#     def __init__(self,questionare):
#         self.questionHtmlName = '晴雨表'
#         self.questionare = questionare
#         self.genHtml = 'questionare.html'
#
#     def createHtml(self):
#
#         # 打开文件，准备写入
#         f = open(self.genHtml, 'w')
#         # 准备相关变量
#         message = """
#         <html>
#         <head></head>
#         <body>
#         <p>%s</p>
#         <p>%s</p>
#         </body>
#         </html>""" % (str1, str2)
#
#         # 写入文件
#         f.write(message)
#         # 关闭文件
#         f.close()
# coding=utf-8
__author__ = 'liu.chunming'
import logging

logging.basicConfig(level=logging.WARNING,
                    filename='./log.txt',
                    filemode='w',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
# use logging
logging.info('this is a loggging info message')
logging.debug('this is a loggging debug message')
logging.warning('this is loggging a warning message')
logging.error('this is an loggging error message')
logging.critical('this is a loggging critical message')
