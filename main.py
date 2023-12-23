import tkinter as tk
from tkinter import filedialog
import os, subprocess, platform
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


def open_file_explorer(path):
    """
    Opens the given path in the system's default file explorer.

    Args:
    path (str): The directory path to open.
    """
    if not os.path.exists(path):
        print("The specified path does not exist.")
        return

    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(["open", path])
    else:  # Linux and other Unix-like systems
        subprocess.Popen(["xdg-open", path])

def listify(mypath):
    '''
    Gathers all .tiff files in a directory.
    Args:
        mypath (str): The path to search for .tiff files.
    Returns:
        justpics (list): A list of paths to .tiff files found in the given directory.
    '''
    listdir = []
    for root, dirs, files in os.walk(os.path.abspath(mypath)):
        for file in files:
            listdir.append(os.path.join(root, file))
    justpics = [dirs for dirs in listdir if dirs.endswith('tiff')]
    return justpics

def breakdown(picslist):
    '''
    Breaks down the file paths into a list of lists for easier parsing.
    Args:
        picslist (list): List of file paths.
    Returns:
        breakdownList (list of lists): Each sublist contains parts of the file path.
    '''
    breakdownList = [imgpath.split('\\')[-4:-1] + [imgpath] for imgpath in picslist]
    return breakdownList

def dictify(breakdownlist):
    '''
    Converts a breakdown list to a nested dictionary for structured access.
    Args:
        breakdownlist (list): A list containing the broken-down file paths.
    Returns:
        dirdict (dict): A nested dictionary representing the directory structure.
    '''
    dirdict = {}
    for k, v, a, d in breakdownlist:
        dirdict.setdefault(k, {}).setdefault(v, {}).setdefault(a, []).append(d)
    return dirdict

def smallestImgDim(breakdownlist):
    '''
    Finds the dimensions of the smallest image in the dataset.
    Args:
        breakdownlist (list): List of broken-down file paths.
    Returns:
        data (dict): Contains dimensions of the smallest image.
    '''
    data = {'min_width': 0, 'min_height': 0, 'min_pix_ct': 0, 'file_path': ""}
    for _, _, _, d in breakdownlist:
        with Image.open(d) as img:
            width, height = img.size
            if width * height > data['min_pix_ct'] or data['min_pix_ct'] == 0:
                data.update({'min_width': width, 'min_height': height, 'min_pix_ct': width * height, 'file_path': d})
    return data

def ensmallenImg(smallestimgdim, newpath):
    '''
    Resizes an image to match the dimensions of the smallest image.
    Args:
        smallestimgdim (dict): Dimensions of the smallest image.
        newpath (str): Path of the image to be resized.
    Returns:
        smallimage (Image): The resized image.
    '''
    image = Image.open(newpath)
    smallimage = image.resize((smallestimgdim['min_width'], smallestimgdim['min_height']))
    return smallimage

def getMaxImages(breakdowndict):
    '''
    Determines the maximum number of images in each secondary subgroup.
    Args:
        breakdowndict (dict): Nested dictionary from `dictify`.
    Returns:
        maxbyweek (dict): Dictionary indicating max images per subgroup.
    '''
    maximgdict = {key: breakdowndict[key] for key in breakdowndict}
    maxbyweek = {}
    for names in maximgdict:
        for items in maximgdict[names]:
            maxbyweek.setdefault(items, []).append(len(maximgdict[names][items]))
    for weeks in maxbyweek:
        maxbyweek[weeks] = max(maxbyweek[weeks])
    return maxbyweek

def makeHeader(dimensions, name):
    '''
    Creates a header image with text.
    Args:
        dimensions (dict): Dimensions for the header.
        name (str): Text to be added to the header.
    Returns:
        background (Image): Header image with text.
    '''
    width, height = dimensions['min_width'], dimensions['min_height']
    fontsize, img_fraction = 1, 0.5
    myfont = ImageFont.truetype("arial.ttf", fontsize)
    background = Image.new("RGB", (width, height), color='black')
    while myfont.getmask(name).getbbox()[2] < img_fraction * background.size[0] and myfont.getmask(name).getbbox()[3] < img_fraction * background.size[1]:
        fontsize += 1
        myfont = ImageFont.truetype("arial.ttf", fontsize)
    write = ImageDraw.Draw(background)
    text_x, text_y = (width - myfont.getbbox(name)[2]) / 2, (height - myfont.getbbox(name)[3]) / 2
    write.text((text_x, text_y), name, fill="white", font=myfont)
    return background

def makeYLegend(dirpath):
    '''
    Generates the first column of the montage grid with headers.
    Args:
        dirpath (str): Root path of the directory.
    Returns:
        sidebar (Image): The first column of the montage grid.
    '''
    dirlist = breakdown(listify(dirpath))
    dirdict = dictify(dirlist)
    heightbyweek = getMaxImages(dirdict)
    dimensions = smallestImgDim(dirlist)
    unit_height = dimensions['min_height']
    height = (sum(heightbyweek.values()) + 2) * unit_height
    sidebar = Image.new('RGB', (dimensions['min_width'], height), color='black')
    y_offset = 2 * unit_height
    for weeks in sorted(heightbyweek.keys()):
        dimensions['min_height'] = heightbyweek[weeks] * unit_height
        weekheader = makeHeader(dimensions, weeks)
        sidebar.paste(weekheader, (0, y_offset))
        y_offset += unit_height * heightbyweek[weeks]
    return sidebar

def makeColumns(dirpath, dirdict, dirlist):
    '''
    Creates the full montage grid.
    Args:
        dirpath (str): Root path of the directory.
    Returns:
        None: Saves the final montage image.
    '''
    dirlist = breakdown(listify(dirpath))
    dirdict = dictify(dirlist)
    heightbyweek = getMaxImages(dirdict)
    dimensions = smallestImgDim(dirlist)
    unit_height, unit_width = dimensions['min_height'], dimensions['min_width']
    height = (sum(heightbyweek.values()) + 2) * unit_height
    width = (1 + sum(len(dirdict[i].keys()) for i in dirdict.keys())) * unit_width
    graphcanvas = Image.new('RGB', (width, height), 'black')
    graphcanvas.paste(makeYLegend(dirpath), (0, 0))
    x_offset, y_offset = unit_width, 0
    for groups in sorted(dirdict.keys()):
        groupheader = makeHeader({'min_width': len(dirdict[groups].keys()) * unit_width, 'min_height': unit_height}, groups)
        graphcanvas.paste(groupheader, (x_offset, y_offset))
        y_offset += unit_height
        for animals in sorted(dirdict[groups].keys()):
            animalheader = makeHeader(dimensions, animals)
            graphcanvas.paste(animalheader, (x_offset, y_offset))
            y_offset += unit_height
            for weeks in sorted(dirdict[groups][animals]):
                for files in sorted(dirdict[groups][animals][weeks]):
                    newimg = Image.open(files)
                    graphcanvas.paste(newimg, (x_offset, y_offset))
                    y_offset += unit_height
                y_offset = unit_height + heightbyweek[weeks] * unit_height
            x_offset += unit_width
            y_offset = 0
    graphcanvas.save(os.path.join(dirpath, f'montague_{datetime.now().strftime("%m.%d.%y")}.tiff'))
    open_file_explorer(dirpath)
    graphcanvas.show()

def select_directory():
    '''
    Opens a dialog to select a directory and sets the entry field with the selected path.
    '''
    directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, directory)

def generate_image():
    '''
    Uses the selected directory to generate the timecourse image.
    '''
    dirpath = directory_entry.get()
    if not dirpath:
        print("Please select a directory.")
        return

    dirlist = breakdown(listify(dirpath))
    dirdict = dictify(dirlist)
    makeColumns(dirpath, dirdict, dirlist)
    print("Image generated successfully.")

# Tkinter GUI setup
root = tk.Tk()
root.title("Montague Timecourse Generator")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

directory_entry = tk.Entry(frame, width=50)
directory_entry.pack(side=tk.LEFT, padx=(0, 10))

browse_button = tk.Button(frame, text="Browse", command=select_directory)
browse_button.pack(side=tk.LEFT)

generate_button = tk.Button(root, text="Generate Image", command=generate_image)
generate_button.pack(pady=(5, 0))

root.mainloop()
