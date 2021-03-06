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

# insert batch mode 0 for train-annotation-points generation, otherwise 1 for the validation
batch_mode = 0

if batch_mode == 0:
    filepath_masks = os.path.abspath(os.path.join(basepath, "Data/train"))
    filepath_raws = os.path.abspath(os.path.join(basepath, "Data/raws"))
    annotation_location = os.path.abspath(os.path.join(basepath, "Data/train-annotation-store"))
else:
    filepath_masks = os.path.abspath(os.path.join(basepath, "Data/val"))
    filepath_raws = os.path.abspath(os.path.join(basepath, "Data/raws"))
    annotation_location = os.path.abspath(os.path.join(basepath, "Data/validation-annotation-store"))

directory_files = [pos_mask_files for pos_mask_files in os.listdir(filepath_masks) if pos_mask_files.endswith('.png')]

data = {}

for x in range(0, len(directory_files)):
    img = (filepath_masks + "\\" + directory_files[x])
    img_with_no_tag = directory_files[x]
    size_of_img = str(os.stat(filepath_raws + "\\" + directory_files[x]).st_size)
    img_capsulated = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    img_capsulated_rgb = cv2.imread(img, cv2.IMREAD_COLOR)
    parent_tag = img_with_no_tag + size_of_img
    contourIndexNo = 0

    data[img_with_no_tag + size_of_img] = {
        'filename': img_with_no_tag,
        'size': os.stat(filepath_raws + '\\' + directory_files[x]).st_size,
        'regions': [
        ],
        'file_attributes': {
            'caption': '',
            'public_domain': 'no',
            'image_url': ''
        }
    }

    k = 0  # enumerator to show the current index
    # of filled list that include polygon points
    # empty list to fill polygon co-vertices
    my_list_point_x = []
    my_list_point_y = []
    # Converting image to a binary image
    # ( black and white only image).
    _, threshold = cv2.threshold(img_capsulated, 110, 255, cv2.THRESH_BINARY)

    # Detecting contours in image.
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)

    # Going through every contours found in the image.
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.001 * cv2.arcLength(cnt, True), True)
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
                d = data[parent_tag]['regions']
                d[contourIndexNo]['shape_attributes']['all_points_x'].append(my_list_point_x[k])
                d[contourIndexNo]['shape_attributes']['all_points_y'].append(my_list_point_y[k])
                k = k + 1
            i = i + 1
        contourIndexNo = contourIndexNo + 1
    maskIndexNo = maskIndexNo + 1

with io.open(
        annotation_location + '\\via_region_data.json',
        'w', encoding='utf8') as outfile:
    str_ = json.dumps(data, cls=NumpyEncoder)
    outfile.write(to_unicode(str_))
