import os
from os.path import isfile, join

dirpath = 'C:\\Users\\Thomas.Henshaw001\\Development\\montague\\2022_Ben'

def listify(mypath):
    listdir = []
    for root, dirs, files in os.walk(os.path.abspath(mypath)):
        for file in files:
            listdir.append(os.path.join(root, file))
    justpics = []
    for dirs in listdir:
        if dirs.endswith('tiff'):
            justpics.append(dirs)
    return justpics

def breakdown(picslist):
    breakdownList = []
    for imgpath in picslist:
        new = imgpath.split('\\')[-4:-1]
        new.append(imgpath)
        breakdownList.append(new)
    return breakdownList

def dictify(breakdownlist):
    dirdict = {}
    for k, v, a, d in breakdownlist:
        if k not in dirdict:
            dirdict[k] = {v:{a:[d]}}
        elif v not in dirdict[k]:
            dirdict[k][v] = {a:[d]}
        elif a not in dirdict[k][v]:
            dirdict[k][v][a] = [d]
        else:
            dirdict[k][v][a].append(d)
    return dirdict



print(dictify(breakdown(listify(dirpath))))
