import os
import cv2

basepath = os.path.dirname(__file__)
filepath = os.path.abspath(os.path.join(basepath, "Data/masks"))
directory_files = [pos_mask_files for pos_mask_files in os.listdir(filepath) if pos_mask_files.endswith('.png')]
font = cv2.FONT_HERSHEY_COMPLEX

for currentImg in range(0, len(directory_files)):
    img_mask = ("Data\\masks\\" + directory_files[currentImg])
    img_raw = ("Data\\raws\\" + directory_files[currentImg])
    img_with_no_tag = directory_files[currentImg]
    img_capsulated_grayscale = cv2.imread(img_mask, cv2.IMREAD_GRAYSCALE)
    img_capsulated_rgb = cv2.imread(img_raw, cv2.IMREAD_COLOR)

    # Converting image to a binary image
    # ( black and white only image).
    _, threshold = cv2.threshold(img_capsulated_grayscale, 110, 255, cv2.THRESH_BINARY)

    # Detecting contours in image.
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
    counterCountInMask = str(len(contours))
    # print(counterCountInMask)
    # Going through every contours found in the image.
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        # # draws boundary of contours.
        cv2.drawContours(img_capsulated_rgb, [approx], 0, (0, 0, 255), 1)

        # Used to flatted the array containing
        # the co-ordinates of the vertices.
        n = approx.ravel()
        i = 0

        for j in n:
            if i % 2 == 0:
                x = n[i]
                y = n[i + 1]
                # String containing the co-ordinates.
                string = str(x) + " " + str(y)

                # # text on remaining co-ordinates.
                cv2.putText(img_capsulated_rgb, string, (x, y),
                            font, 0.5, (0, 255, 0))
                # cv2.imshow('test.png', img_capsulated_rgb)
                # cv2.waitKey(0)
            i = i + 1
    # cv2.imshow('test.png', img_capsulated_rgb)
    # cv2.waitKey(0)
    cv2.imwrite("Data\\raws-with-points\\" + str(currentImg) + ".png", img_capsulated_rgb)
print("done")
