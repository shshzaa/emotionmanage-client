#coding=utf-8
#!/usr/bin/python
import os
import datetime
import subprocess
import time
import psutil


def isStarted():
    ctime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    fp = open('./log.txt','r')
    logger = fp.readlines()
    for info in logger:
        print(info[0:10])
        print(info[-8:])
        if info[0:10] == ctime and info[-8:] == 'success':
            return True
    return False
def open_app(app_dir):
    os.startfile(app_dir)
if __name__ == "__main__":
    programName = 'barometer.exe'
    h=18
    m=31
    sleep_interval = 43200
    intervel = 2
    app_dir = r'./barometer.exe'
    openState = False
    while True:

        finishstate = isStarted()
        print(finishstate)
        if finishstate:
            time.sleep(sleep_interval)
        else:
            print('f')
            now = datetime.datetime.now()
            if (now.hour - h) % intervel == 0 and now.minute == m:
                if programName in (p.name() for p in psutil.process_iter()):
                    print('已开启')
                    time.sleep(20)
                else:
                    subprocess.Popen(app_dir)
            else:
                time.sleep(20)


