import os
from os import path
import numpy as np
import cv2

basepath = path.dirname(__file__)  # get file basepath for folder batch processing
filepath = path.abspath(path.join(basepath, "Data/masks-cleaned"))
raw_mask_files = [pos_xml for pos_xml in os.listdir(filepath) if pos_xml.endswith('.png')]


for x in range(0, len(raw_mask_files)):  # loop in the directory to threshold each different unique label
    image_8bit = cv2.imread(filepath + "\\" + raw_mask_files[x], 0)
    image_16bit_normalized = image_8bit / 255;
    img16 = np.uint16(image_16bit_normalized)
    cv2.imwrite("C:\\Users\\BURAK\\Desktop\\binarymask2json\\Data\\masks-16bit-cleaned\\" + str(raw_mask_files[x]), img16)  # write the file onto the disk
