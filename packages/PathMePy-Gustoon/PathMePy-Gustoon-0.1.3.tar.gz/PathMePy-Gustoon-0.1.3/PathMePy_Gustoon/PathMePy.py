import os
import platform
import site
import sys

def PathMePyDir(path):
    path = os.path.abspath(path)
    if platform.system() != "Windows" and platform.system() != "Linux" :
        print("I don't have MAC OS so you need to add manualy to Path " + path)
    if platform.system() == "Windows" :
        os.system('set Path="%Path%;' + path + '"')
    elif platform.system() == "Linux":
        os.system('export PATH=$PATH:' + path)

def PathMePyUserScriptFolder():
    path = site.getusersitepackages()
    if platform.system() != "Windows" and platform.system() != "Linux" :
        print("I don't have MAC OS so you need to add manualy to Path the user site package folder.")
    if platform.system() == "Windows" :
        os.system('set Path="%Path%;' + path + '"')
    elif platform.system() == "Linux":
        os.system('export PATH=$PATH:' + path)