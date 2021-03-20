from data.art.training_images import text_files, processed
from creation.blocks import slice_array
from image_processing.process_images import load_images_from_folder
import os
import h5py
import numpy as np


def read_h5(filename, folder):
    for files in os.listdir(folder):
        if files == filename:
            with h5py.File(filename, "r") as q:
                data = q["colour_images/test_data"].value
                print(data)
                print(data.shape)
                return data
    print("No file found of name: " + filename)


grids = read_h5("data.h5", os.path.dirname(text_files.__file__))
