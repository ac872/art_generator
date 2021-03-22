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

from src.image_processing.process_images import load_images_from_folder
import os
import h5py
import numpy as np


def slice_array(array, num_rows, num_cols):
    h, w = array.shape
    return (array.reshape(h // num_rows, num_rows, -1, num_cols)
            .swapaxes(1, 2)
            .reshape(-1, num_rows, num_cols))


def chop_arrays_to_grids(block_length, folder):
    images = load_images_from_folder(folder)
    images = [i[0] for i in images]  # Remove filenames
    grids = []

    # Create list of smaller arrays from the larger array
    for i in images:
        chopped_np_arrays = [slice_array(i[:, :, x], block_length, block_length) for x in range(3)]
        gbr = np.stack(chopped_np_arrays, axis=3)
        grids.append(gbr)

    # Combine the numpy arrays into a list
    square_grids = np.stack([i for i in grids])
    return square_grids


def save_to_hf(filename, folder, data_grid):
    for files in os.listdir(folder):
        if files == filename:
            with h5py.File(filename, "w") as f:
                f.clear()
                group = f.create_group("colour_images")
                group.create_dataset("test_data", data=data_grid)
                print(list(f.keys()))
            return
    print("No file found of name: " + filename)
