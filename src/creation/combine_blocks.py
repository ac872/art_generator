from data.art.training_images import text_files, processed
from creation.blocks import combine_array
from image_processing.process_images import load_images_from_folder
from random import seed, randint
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

    total_blocks = (h * w) / 100
    print(total_blocks)
    new_image = None
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


    blocks = np.stack([i for i in list_of_blocks])
    print(blocks.shape)
    # blocks = combine_array(blocks, h, w)
    # print(blocks.shape)





generated_image = create_image(120, 640, grids)
# cv2.imshow("CroppedImage", generated_image)  # Show Cropped Image
# cv2.waitKey(0)
