import sys
from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = "C:\\Python36\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Python36\\tcl\\tk8.6"

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

includes = [r'queue',r'idna.idnadata']

include_files = ["C:\\Python36\DLLs\\tcl86t.dll",
                 "C:\\Python36\DLLs\\tk86t.dll",
                 'icon_32.ico',
                 'question.json',
                 'log.txt',
                 'bg1400x800.jpg',
                 'logo.jpg',
                 'tip.png',
                 'loginfirst.png']

options = {
'build_exe':{ 'includes':includes,'include_files':include_files},
}

executables = [Executable(script='barometer.py', base=base, targetName='barometer.exe')]

setup(
    name="barometer",
    version="1.0.0",
    author='diaokongzhongxin',
    author_email='zhangpengjie1993@163.com',
    description="dangjian barometer",
    options=options,
    executables=executables,
)