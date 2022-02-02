# import module and packages
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter import *
import tkinter.font as ft
import os
from datetime import date
from datetime import datetime
import natsort
import subprocess
import argparse
from time import sleep
from collections import OrderedDict

# args
parser = argparse.ArgumentParser(description="Please Type Names of setup.txt, Set.exe, and Run.exe")
parser.add_argument("--setup", required=False, default="./setup.txt", help="Type the Setup.txt files's path and name, e.g. ./setup.txt")
parser.add_argument("--set", required=False, default="./set_NKFADC500_1CH.exe", help="Type the Set.exe files's path and name, e.g. ./set.exe")
parser.add_argument("--run", required=False, default="./run_NKFADC500_1CH.exe", help="Type the Run.exe files's path and name, e.g. ./run.exe")
args = parser.parse_args()
print(args.setup)
# ------------------------ Global Variables
varInputXpos = 270;
unitsXpos = 375;
wrapLength = 250;
btnFramePadX = 470;
btnFramePadY = 10;
btnRelX = 0.5;
btnRelY = 0.05;
labelPosX = 10;
isAllValidVar = []
VariableData = []
Operatingbtns=OrderedDict()
OperatingEntries=OrderedDict()
OperatingComboBoxes=OrderedDict()
OperatingClassess=OrderedDict()
nameSetup=0;
nameSetExec=0;
nameRunExec=0;

# Read default var
numOfVar = 15; defaultVar = []; defaultVarIndex = 0
f = open("./setup.txt", "r");
for i in range(numOfVar):
    var = f.readline().split()
    defaultVar.append(var[0])
    isAllValidVar.append(1)
    VariableData.append(None)
f.close()

# ------------------------ Frame, Varialbes ------------------------
## varialbes 
pos_y = 10
hlt = 1
hlbgNormal = "black" # Background -> normal state, not clicked
hlCAllowed = "green" 
hlCNotAllowed = "red" 

## Functions
def updateYposAndIndex(degree=30):
    global pos_y;
    global defaultVarIndex
    pos_y += degree; 
    defaultVarIndex +=1;
    return pos_y, defaultVarIndex

def updateBtnPosition():
    global btnRelY;
    btnRelY += 0.15
    return btnRelY;
    
