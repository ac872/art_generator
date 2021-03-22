"""
MIT License

Copyright (c) 2021 Arbri Chili

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import cv2
import os


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename), 1)
        if img is not None:
            images.append([img, filename])  # Append image and image filename
    return images


def crop_images(images):
    # Cropped from top left of the image
    y = 0
    x = 0
    # Size of image:
    # Ensure image size is 640x640
    h = 640
    w = 640
    for row in images:
        image = row[0]
        row[0] = image[x:w, y:h]
        row[1] = str(h) + "x" + str(w) + row[1]
        # cv2.imshow("CroppedImage", row[0])  # Show Cropped Image
        # cv2.waitKey(0)
    return images


def save_images(images, folder):
    print(folder)
    for row in images:
        img = row[0]
        filename = row[1]
        location = os.path.join(folder, filename)
        print(location)
        cv2.imwrite(location, img)
