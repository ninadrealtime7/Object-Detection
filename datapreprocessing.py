PASCAL_CLASSES = [
    'none',
    'aeroplane',
    'bicycle',
    'bird',
    'boat',
    'bottle',
    'bus',
    'car',
    'cat',
    'chair',
    'cow',
    'diningtable',
    'dog',
    'horse',
    'motorbike',
    'person',
    'pottedplant',
    'sheep',
    'sofa',
    'train',
    'tvmonitor'
]

# Fill in the classes you want to retain

classesINeed = ['none', 'cat','dog']

# Define the relevant directories

xmlDirectory = 'I:/realtimedataset/VOCdevkit/VOC2012/Annotations/'

modifiedXmlDir = 'I:/realtimedataset/cars/'

JPEGdirectory = 'I:/realtimedataset/VOCdevkit/VOC2012/JPEGImages/'

modifiedJPEGdir = 'I:/realtimedataset/cars/'

listFile = 'I:/realtimedataset/trainval.txt'

labelMap = 'I:/realtimedataset/labelmap_voc.prototxt'

listfile = open(listFile, 'w')
labelmap = open(labelMap, 'w')

import os
from shutil import copyfile
from os.path import isfile, join

# Get all the xml files into list
onlyfiles = [f for f in os.listdir(xmlDirectory) if isfile(join(xmlDirectory, f))]

# For saving the class - file dictionary
fileDict = {}

i = 0

# for limiting number of images
imgnum = 0

for claz in classesINeed:
    fileDict[claz] = []
    # generate labelmap file
    labelmap.write('item {\n  name: "' + claz + '"\n  label: ' + str(i) + '\n  display_name: "' + claz + '"\n}\n')
    i += 1

labelmap.close()
# Parse each XML file
import xml.etree.ElementTree as ET

for filename in onlyfiles:
    filelink = join(xmlDirectory, filename)
    tree = ET.parse(filelink)
    root = tree.getroot()
    objs = root.findall('object')
    objNum = 0
    for obj in objs:
        objNum += 1
        currentObj = obj.find('name').text
        if currentObj not in classesINeed:
            root.remove(obj)
            objNum -= 1
        else:
            fileDict[currentObj].append(filename)

    if objNum == 0:
        continue  # drop the file, there are no objects of 'interest '
    else:  # write to the file as xml to the new folder
        fwrite = open(modifiedXmlDir + filename, 'wb')
        tree.write(fwrite)
        fwrite.close()

        # copy the corresponding JPEG to modifiedJPEGDIr
        copyfile(JPEGdirectory + filename[:-3] + 'jpg', modifiedJPEGdir + filename[:-3] + 'jpg')
        imgnum += 1

        # make entry in the list file required for LMDB
        listfile.write('VOC2012/newJPEGImages/' + filename[:-3] + 'jpg' + ' VOC2012/newAnnotations/' + filename + '\n')



# print "found "+ str(objNum ) + " object(s) in " + filename[:-3]

listfile.close()
print(len(fileDict['car']))