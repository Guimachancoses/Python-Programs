# Program to force start application, case user close.

import os
import psutil
from time import sleep
  
while True:
    # check if chrome is open
    check = "3CXDesktopApp.exe" in (i.name() for i in psutil.process_iter())
    if check == True:
        print()
    else:
        os.startfile(r'C:\Users\guilhermemachado\AppData\Local\Programs\3CXDesktopApp\3CXDesktopApp.exe')
        os.startfile(r'C:\Users\guilhermemachado\AppData\Local\Programs\3CXDesktopApp\app\3CXDesktopApp.exe')
    sleep(15)
