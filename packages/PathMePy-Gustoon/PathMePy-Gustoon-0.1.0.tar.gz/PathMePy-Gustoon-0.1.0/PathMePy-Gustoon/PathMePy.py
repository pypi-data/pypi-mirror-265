import os
import platform
import site
import sys

if platform.system() != "Windows" and platform.system() != "Linux" :
    print("I don't have MAC OS so I don't know how to change Path")
    sys.exit(1)

def PathMePyDir(path):
    path = os.path.abspath(path)
    if platform.system() == "Windows" :
        os.system('set Path="%Path%;' + path + '"')
    elif platform.system() == "Linux":
        os.system('export PATH=$PATH:' + path)

def PathMePyUserScriptFolder():
    path = site.getusersitepackages()
    if platform.system() == "Windows" :
        os.system('set Path="%Path%;' + path + '"')
    elif platform.system() == "Linux":
        os.system('export PATH=$PATH:' + path)