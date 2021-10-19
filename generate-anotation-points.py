import io
import json
import os
import cv2
import numpy as np
from numpy.compat import unicode

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

font = cv2.FONT_HERSHEY_COMPLEX


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


size_of_img = 0
maskIndexNo = 0
contourIndexNo = 0
basepath = os.path.dirname(__file__)
filepath = os.path.abspath(os.path.join(basepath, "Data/"))
directory_files = [pos_mask_files for pos_mask_files in os.listdir(filepath) if pos_mask_files.endswith('.png')]

data = {

}

for x in range(0, len(directory_files)):
    # print(directory_files[x])
    # print(os.stat('Data\\' + directory_files[x]).st_size)
    img = ("Data\\" + directory_files[x])
    img_with_no_tag = directory_files[x]
    size_of_img = str(os.stat('Data\\' + directory_files[x]).st_size)
    img_capsulated = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    img_capsulated_rgb = cv2.imread(img, cv2.IMREAD_COLOR)
    parent_tag = img_with_no_tag + size_of_img
    contourIndexNo = 0

    data[img_with_no_tag + size_of_img] = {
            'filename': img_with_no_tag,
            'size': size_of_img,
            'regions': [
            ],
            'file_attributes': {
                'caption': '',
                'public_domain': 'no',
                'image_url': ''
            }
        }


    # print(*listTest, sep="{}")
    # data.append(listTest)

    k = 0  # enumerator for in
    # empty list
    my_list_point_x = []
    my_list_point_y = []
    whole_my_list_points_x = []
    whole_my_list_points_y = []
    # Converting image to a binary image
    # ( black and white only image).
    _, threshold = cv2.threshold(img_capsulated, 110, 255, cv2.THRESH_BINARY)

    # Detecting contours in image.
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
    counterCountInMask = str(len(contours))
    # print(counterCountInMask)
    # Going through every contours found in the image.
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        # # draws boundary of contours.
        # cv2.drawContours(img2, [approx], 0, (0, 0, 255), 5)
        data[parent_tag]['regions'].append({
            'shape_attributes': {
                'name': 'polygon',
                'all_points_x': [

                ],
                'all_points_y': [

                ]},
            'region_attributes': {
                'name': 'rooftop',
                'type': 'rooftop',
                'image_quality': {
                    'good': True
                }
            }
        })
        # Used to flatted the array containing
        # the co-ordinates of the vertices.
        n = approx.ravel()
        i = 0

        for j in n:
            if i % 2 == 0:
                x = n[i]
                y = n[i + 1]
                my_list_point_x.append(x)
                my_list_point_y.append(y)
                # String containing the co-ordinates.
                # string = str(x) + " " + str(y)
                d = data[parent_tag]['regions']
                d[contourIndexNo]['shape_attributes']['all_points_x'].append(my_list_point_x[k])
                d[contourIndexNo]['shape_attributes']['all_points_y'].append(my_list_point_y[k])
                # # text on remaining co-ordinates.
                # cv2.putText(img_capsulated_rgb, string, (x, y),
                #             font, 0.5, (0, 255, 0))
                # cv2.imshow('test.png', img_capsulated_rgb)
                # cv2.waitKey(0)
                k = k + 1
            i = i + 1
        contourIndexNo = contourIndexNo + 1
        # print("contourIndexNo: ", contourIndexNo)
    maskIndexNo = maskIndexNo + 1
    # print("maskIndexNo: ", maskIndexNo)

with io.open(
        'C:\\Users\\BURAK\\Desktop\\binarymask2json\\data.json',
        'w', encoding='utf8') as outfile:
    str_ = json.dumps(data, cls=NumpyEncoder)
    outfile.write(to_unicode(str_))

    # for count in range(0, len(data)):
    #     str_ = json.dumps(data[count].items(), cls=NumpyEncoder)
    #     outfile.write(to_unicode(str_))
