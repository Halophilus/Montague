# MONTAGUE - README DOCUMENT

![Title](/docs/title.png)

## Introduction
The Montague Timecourse Image Generator is a Python application intended to create a visual grid montage of .tiff images taken over a series of timepoints. It's particularly useful for visualizing time lapse images of different subjects (such as animals in a study) across various time points. The application allows for the organization and comparison of images in a structured format, where each row and column in the grid represents different time points and subjects, respectively.

## Features
- **Directory Selection**: Users can select the directory containing the images to be used for the time-lapse montage on a simple GUI.
- **Automated Image Process**: The application automatically process all images within the directory
- **Dynamic Grid Layout**: The grid layout adjusts dynamically based on the number of images per subject.
- **Hierarchical Label Structure**: The script allows for arbitrary categorical hierarchies to distinguish different animal groups.

## Installation
Ensure Python 3.x is installed on your system.

### Dependencies
This application relies on several Python libraries
- Tkinter for the GUI.
- Pillow for image processing.

These can be installed through the terminal using pip:
```bash
pip install Pillow tkinter
```

## Usage
The proper usage of this script requires a well-formed directory of images based on the following convention:

1. **Overall Structure**: The script is designed to handle a three-level directory hierarchy.
    - The top level represents primary categories, such as experimental groups.
    - The secondary level represents the IDs of each instance being recorded.
    - The innermost level represents the images, named for the individual timepoints at which pictures were taken.
    - Each of those folders contain 0 or more images, and are grouped by a shared naming convention (i.e., all images named 'week 1' will be shown in the same row)

2. **Primary Categories**: Sorted like this in the outer directory:
```
Timecourse_Images/
├── Category_A/
├── Category_B/
└── Category_C/
``` 
3. **Subdirectories**: Stored within each primary category, generally represent animal IDs:
```
Condition_A/
├── Animal_1/
├── Animal_2/
└── Animal_3/
```
4. **Image Files**: Their placement on the grid is determined by their name, which should correspond with a timepoint. Images with the same name are grouped along the same row in the montage
```
Animal_1/
├── Week_1.tiff
├── Week_2.tiff
└── Week_3.tiff
```
5. **Overall Directory**: The directory as a whole should look something like this:
```
Timecourse_Images/
├── Condition_A/
│   ├── Animal_1/
│   │   ├── Week_1.tiff
│   │   ├── Week_2.tiff
│   │   └── Week_3.tiff
│   ├── Animal_2/
│   │   ├── Week_1.tiff
│   │   └── Week_2.tiff
│   └── Animal_3/
│       └── Week_1.tiff
└── Condition_B/
    ├── Animal_4/
    │   ├── Week_1.tiff
    │   └── Week_2.tiff
    └── Animal_5/
        ├── Week_1.tiff
        └── Week_2.tiff

```
6. **Predicted Output**
```
Montage Grid Layout:
+--------------------------------------------------------------------+
|        |        Condition_A       |           Condition_B          |
|        |  Animal_1  |  Animal_2   | Animal_3 | Animal_4 | Animal_5 |
+--------------------------------------------------------------------+
| Week_1 |    Img     |     Img     |   Img    |   Img    |   Img    |
| Week_2 |    Img     |     Img     |          |   Img    |   Img    |
| Week_3 |    Img     |             |          |          |          |
+--------------------------------------------------------------------+
```
- **X-AXIS**: Primary categories (outer) and animal IDs (or similar, depending on application).
- **Y-AXIS**: Date of image collection, indicated by image naming convention.
- The montage allows for a side-by-side comparison of subjects across different conditions and time points.

7. **GUI Usage**:

![Montague GUI](/docs/gui.png)

- Run the file in a Python interpreter.
- Press `Browse` to locate a folder directory within your file explorer.
- Once a directory of the above format is selected, press `Generate Image`
- Depending on the size of the images and the number of images being processed, this may take several minutes.
- Once done, the image and the folder it is saved in should pop up, named for the date and time at which the image was generated.

## Troubleshooting
- This specific version was created for `*.tiff` images, but could easily be refactored for other formats.
- Double check uniform image naming to ensure accuracy of results, making sure each animal ID is in its proper category.
- If you have any issues with the script, make sure that Pillow and Python are installed correctly.

## Contributing
- I no longer have any personal use for this script as I have changed professions.
- During my time working in a limb-regeneration lab, it was crucial to make timecourse analyses to analyze limb growth in different animals under different conditions.
- Performing this process manually was incredibly difficult, so hopefully this tool makes it easier for at least one person.
- If you have any ideas to expand on this or revise it, feel free to fork this repository. This project is relatively small and could be easily expanded upon.

## License

The Montague Timecourse Generator is open-sourced software licensed under the [MIT License](LICENSE.txt).


