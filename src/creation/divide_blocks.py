from data.art.training_images import text_files, processed
from creation.blocks import slice_array
from image_processing.process_images import load_images_from_folder
import os
import h5py
import numpy as np


#     green = i[:, :, 0]
#     green = slice_array(green, 10, 10)
#     blue = i[:, :, 1]
#     blue = slice_array(blue, 10, 10)
#     red = i[:, :, 2]
#     red = slice_array(red, 10, 10)
#     # GBR = np.stack([i[:, :, x] for x in range(0, 2)], axis=3)
#     GBR = np.stack([green, blue, red], axis=3)
#     print(GBR.shape)
#     grids.append(GBR)

def chop_arrays_to_grids():
    # Refactor to include dynamic file name and dynamic images list when method declared?
    # Currently loads all images from specific directory
    images = load_images_from_folder(os.path.dirname(processed.__file__))
    images = [i[0] for i in images]  # Remove filenames
    grids = []

    # Create list of smaller arrays from the larger array
    for i in images:
        chopped_np_arrays = [slice_array(i[:, :, x], 10, 10) for x in range(3)]
        gbr = np.stack(chopped_np_arrays, axis=3)
        grids.append(gbr)

    # Combine the numpy arrays into a list
    square_grids = np.stack([i for i in grids])
    return square_grids


def save_to_hf(filename, folder, data_grid):
    for files in os.listdir(folder):
        if files == filename:
            with h5py.File(filename, "w") as f:
                group = f.create_group("colour_images")
                group.create_dataset("test_data", data=data_grid)
                print(list(f.keys()))

            return
    print("No file found of name: " + filename)


chopped = chop_arrays_to_grids()

save_to_hf("data.h5", os.path.dirname(text_files.__file__), chopped)

