from data.art.training_images import text_files, processed
from data.art.generated_images import first_batch_test
from creation.blocks import combine_array
from image_processing.process_images import load_images_from_folder
from random import seed, randint
import time
import datetime
import os
import h5py
import cv2

import numpy as np


def read_h5(filename, folder):
    for files in os.listdir(folder):
        if files == filename:
            with h5py.File(filename, "r") as q:
                data = np.array(q["colour_images/test_data"])
                return data
    print("No file found of name: " + filename)


grids = read_h5("data.h5", os.path.dirname(text_files.__file__))


def is_multiple_of(num, multiple=10):
    while not num % multiple == 0:
        num -= 1
    yield num


def create_image(h, w, data):
    block_length = 10
    if h < block_length or w < block_length:
        return ValueError
    h = next(is_multiple_of(h, block_length))
    w = next(is_multiple_of(w, block_length))

    total_blocks = (h * w) / (block_length * block_length)
    list_of_blocks = []
    number_of_images = data.shape[0]
    number_of_blocks = data.shape[1]
    seed()
    for num in range(int(total_blocks)):
        image_num = randint(0, number_of_images - 1)
        single_image = data[image_num, :, :, :, :]
        block_num = randint(0, number_of_blocks - 1)
        single_block = single_image[block_num, :, :, :]
        list_of_blocks.append(single_block)
        # chopped_np_arrays = [slice_array(i[:, :, x], 10, 10) for x in range(3)]
        # gbr = np.stack(chopped_np_arrays, axis=3)
        # grids.append(gbr)

    blocks = np.stack([i for i in list_of_blocks])

    # Implement loop and/or list comprehension
    green = blocks[:, :, :, 0]
    green = combine_array(green, h, w)
    blue = blocks[:, :, :, 1]
    blue = combine_array(blue, h, w)
    red = blocks[:, :, :, 2]
    red = combine_array(red, h, w)

    blocks = np.stack([green, blue, red], axis=2)
    return blocks


generated_image = create_image(2000, 2000, grids)


t = time.localtime()
current_time = time.strftime("%d-%m-%Y_%H_%M_%S", t)
image_save_location = os.path.join(os.path.dirname(first_batch_test.__file__), current_time + ".jpg")
cv2.imshow("CroppedImage", generated_image)  # Show Cropped Image
cv2.waitKey(0)
cv2.imwrite(image_save_location, generated_image)
