from msilib.schema import Control
import os
from os.path import isfile, join
from PIL import Image, ImageDraw, ImageFont

dirpath = 'C:\\Users\\Thomas.Henshaw001\\Development\\montague\\2022_Ben\\ML_amp timecourse'

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

def smallestImgDim(breakdownlist):
    data = {'min_width':0,'min_height':0,'min_pix_ct':0,'file_path':""}
    for k, v, a, d in breakdownlist:
        with Image.open(d) as img:
            width, height = img.size
            if width*height > data['min_pix_ct'] or data['min_pix_ct'] == 0:
                data['min_width'] = width
                data['min_height'] = height
                data['min_pix_ct'] = width*height
                data['file_path'] = d
    return data

def ensmallenImg(smallestimgdim, newpath):
    image = Image.open(newpath)
    smallimage = image.resize((smallestimgdim['min_width'],smallestimgdim['min_height']))
    smallimage.save(newpath)

def getMaxImages(breakdowndict):
    maximgdict = {}
    groupslist = list(breakdowndict.keys())
    for key in groupslist:
        maximgdict.update(breakdowndict[key])
    maxbyweek = {}
    nameslist = list(maximgdict.keys())
    for names in nameslist:
        for items in maximgdict[names]:
            if items not in maxbyweek:
                maxbyweek[items] = [len(maximgdict[names][items])]
            else:
    for weeks in maxbyweek:
        maxentry = {weeks: max(maxbyweek[weeks])}
        maxbyweek.update(maxentry)
    return maxbyweek
   
def makeBanner(dimensions, name):
    width = dimensions['min_width']
    height = dimensions['min_height']
    myFont = ImageFont.truetype("Arial.ttf", 16)
    background = Image.new(mode = "RGB", size = (width, height), color = 'white')
    w, h = draw.textsize(name, font = myFont)
    draw = ImageDraw.draw(background)
    draw.text((((width - w)/2),(height - h)/2), name, fill = "white")
    return background







test1 = dictify(breakdown(listify(dirpath)))

print(getMaxImages(test1))



