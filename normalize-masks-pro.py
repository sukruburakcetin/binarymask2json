import os
from os import path
import cv2

basepath = path.dirname(__file__)  # get file basepath for folder batch processing
filepath = path.abspath(path.join(basepath, "Data/masks"))
raw_mask_files = [pos_xml for pos_xml in os.listdir(filepath) if pos_xml.endswith('.png')]

d = {}
for x in range(0, len(raw_mask_files)):  # loop in the directory to threshold each different unique label
    raw_mask_file = cv2.imread(filepath + "\\" + raw_mask_files[x], 0)
    raw_mask_file2 = cv2.imread(filepath + "\\" + raw_mask_files[x], cv2.IMREAD_UNCHANGED)
    for y in range(1, 65535):
        d["mask" + str(y)] = cv2.inRange(raw_mask_file2, y, y) # extract the grayscale color value corresponding to the given range
        d["segmented_img" + str(y)] = cv2.bitwise_and(raw_mask_file, raw_mask_file, mask= d["mask" + str(y)])  # Create a empty Mat and fill it
        # cv2.imwrite(path.join(basepath, "Data\\masks-cleaned\\") + raw_mask_files[x] + ".png",   d["segmented_img" + str(y)])
        d["contours" + str(y)],  d["hierarchy" + str(y)] = cv2.findContours(d["segmented_img" + str(y)], cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)  # find contours
        cv2.drawContours(raw_mask_file, d["contours" + str(y)], -1, 255, -1)   # draw each contour on the same empty mat(inside)
        cv2.drawContours(raw_mask_file, d["contours" + str(y)], -1, 0, 0)  # draw each contour on the same empty mat(lines)
    # cv2.rectangle(raw_mask_file, (0, 0), (511, 511), 255, 1)
    cv2.imwrite(path.join(basepath, "Data\\masks-cleaned\\") + raw_mask_files[x], raw_mask_file) # write the file onto the disk