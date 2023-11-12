import shutil
from PIL import Image
import pytesseract
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askdirectory
import os

resultDirName = 'ocr_search_results'
queries = ['linkedin']

root = Tk()
root.withdraw()
directory = askdirectory()

numFilesInRootDir = 0
# Iterate directory
for path in os.listdir(directory):
    # check if current path is a file
    if os.path.isfile(os.path.join(directory, path)):
        numFilesInRootDir += 1

numFilesSearched = 0
numFileResults = 0

if not os.path.exists(resultDirName):
    os.makedirs(resultDirName)

# Remove all files in the directory
for filename in os.listdir(resultDirName):
    file_path = os.path.join(resultDirName, filename)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
    except FileNotFoundError:
        print('err')
        continue


def match(query, text):
    for str in query:
        if str in text:
            return True
    return False


for filename in os.listdir(directory):
    numFilesSearched+=1
    if filename == '.DS_Store':
        continue
    file_path = os.path.join(directory, filename)
    try:
        img1 = np.array(Image.open(file_path))
    except (OSError, Image.UnidentifiedImageError):
        continue

    text = pytesseract.image_to_string(img1)
    if match(queries, text) == True:
        numFileResults+=1
        result_file_path = os.path.join(resultDirName, os.path.basename(file_path))
        shutil.copyfile(file_path, result_file_path)
    print('Searched ' + str(numFilesSearched) + ' of ' + str(numFilesInRootDir) + ' files with ' + str(numFileResults) + ' matches')
print('Done!')
root.destroy()

