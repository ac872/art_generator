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

from random import seed, randint
import os
import h5py
import numpy as np


def read_h5(filename, folder):
    for files in os.listdir(folder):
        if files == filename:
            with h5py.File(filename, "r") as q:
                data = np.array(q["colour_images/test_data"])
                return data
    print("No file found of name: " + filename)


def is_multiple_of(num: int, multiple: int):
    while not num % multiple == 0:
        num -= 1
    yield num


def combine_array(arr, h, w):
    n, num_rows, num_cols = arr.shape
    return (arr.reshape(h // num_rows, -1, num_rows, num_cols)
            .swapaxes(1, 2)
            .reshape(h, w))


def create_image(h, w, data, block_length):
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
