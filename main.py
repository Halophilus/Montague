from msilib import make_id
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


#Takes unparsed list of files, unit time, and experimental subgroup and returns the details about the smallest image in a dictionary
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

#Takes return from previous function and the path of the image being resized and returns the smaller image
def ensmallenImg(smallestimgdim, newpath):
    image = Image.open(newpath)
    smallimage = image.resize((smallestimgdim['min_width'],smallestimgdim['min_height']))
    return smallimage

#Takes parsed dictionary and returns a dictionary for the max number of files in each secondary subgroup, this determines the height of the y-axis as it relates to the grid
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
                maxbyweek[items].append(len(maximgdict[names][items]))
    for weeks in maxbyweek:
        maxentry = {weeks: max(maxbyweek[weeks])}
        maxbyweek.update(maxentry)
    return maxbyweek


#Takes dictionary from previous function and a string that represents the text to be added to the image, used to make side-headers for each subgroup
def makeHeader(dimensions, name):
    width = dimensions['min_width']
    height = dimensions['min_height']
    myFont = ImageFont.truetype("arial.ttf", 16)
    background = Image.new(mode = "RGB", size = (width, height), color = 'black')
    w, h = draw.textsize(name, font = myFont)
    draw = ImageDraw.draw(background)
    draw.text((((width - w)/2),(height - h)/2), name, fill = "white")
    return background


#Generates the first column of the montage grid, leaving two spaces at the top for the subgroup headers. The height of each y-axis subgroup is determined by the maximum number of files present in that subgroup. The order of the subgroup is determined alphabetically
def makeYLegend(dirpath):
    dirlist = breakdown(listify(dirpath))
    dirdict = dictify(dirlist)
    heightbyweek = getMaxImages(dirdict)
    dimensions = smallestImgDim(dirlist)
    unit_height = dimensions['min_height']
    height = (sum(heightbyweek.values()) + 2)*dimensions['min_height']
    sidebar = Image.new('RGB', (dimensions['min_width'], height))
    x_offset = 0
    while x_offset < 2 * unit_height:
        blankheader = makeHeader(dimensions, '')
        sidebar.paste(blankheader, (x_offset, 0))
        x_offset += unit_height
    for weeks in sorted(heightbyweek.keys()):
        dimensions['min_height'] = heightbyweek[weeks] * unit_height
        weekheader = makeHeader(dimensions, weeks)
        sidebar.paste(weekheader, (x_offset, 0))
        x_offset += unit_height
    return sidebar

def makeColumns(breakdowndict)
print(dictify(breakdown(listify(dirpath))))



