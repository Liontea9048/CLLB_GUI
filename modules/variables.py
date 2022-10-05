# import module and packages
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter import *
import tkinter.font as ft
import os
from datetime import date
from datetime import datetime
import natsort
import argparse
from time import sleep
from collections import OrderedDict
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import collections
import natsort

# args
parser = argparse.ArgumentParser(description="Please Type Names of setup.txt, Set.exe, and Run.exe")
parser.add_argument("--setup", required=False, default="../CLLB_DAQ/bin/setup.txt", help="Type the Setup.txt files's path and name, e.g. ./setup.txt")
parser.add_argument("--set", required=False, default="../CLLB_DAQ/bin/set_CLLB_DAQ", help="Type the Set.exe files's path and name, e.g. ./set.exe")
parser.add_argument("--run", required=False, default="../CLLB_DAQ/bin/run_CLLB_DAQ", help="Type the Run.exe files's path and name, e.g. ./run.exe")
args = parser.parse_args()
print(args.setup)
# ------------------------ Global Variables
varInputXpos = 270;
unitsXpos = 375;
wrapLength = 250;
btnFramePadX = 470;
btnFramePadY = 10;
plotFramePadX = 730;
plotFramePadY = 10;
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
numbering_ReadFile = 0;
running = 1
isStart = [0]
sglg = [0, 0]
isStopped = [0]

## ------------------------ Plotting Variables
maximumChannel = 4096; 
folderPath = "./waveFiles"

# Read default var
numOfVar = 15; defaultVar = []; defaultVarIndex = 0
varStrings = ["Acq", "HV", "RL", "PTI", "AWD", "DT", "IPP", "PSW", "AM", "PTSD", "TBRT", "IP", "Data", "WF"]

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
    
