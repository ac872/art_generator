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
from typing import Union

from src.image_processing.process_images import load_images_from_folder, crop_images, save_images
from src.image_processing.divide_blocks import chop_arrays_to_grids, save_to_hf
from src.image_processing.combine_blocks import create_image, read_h5
import cv2
import os
import sys
import time
import pathlib

folder_path = os.path.dirname(pathlib.Path(__file__).parent.absolute())
processed = os.path.join(folder_path, "art_data/art/input_images/processed")
unprocessed: Union[str, str] = os.path.join(folder_path, "art_data/art/input_images/unprocessed")
output_imgs = os.path.join(folder_path, "art_data/art/output_images")
h5_data_folder = os.path.join(folder_path, "art_data/h5_files")


block_length = 40
img_width = 400
img_height = 400


def process_images():
    raw_img_filepath = unprocessed
    raw_imgs = load_images_from_folder(raw_img_filepath)
    processed_imgs = crop_images(raw_imgs)
    processed_img_filepath = processed
    save_images(processed_imgs, processed_img_filepath)
    print("Images processed")
    pass


def is_multiple_of(num: int, multiple: int) -> int:
    while not num % multiple == 0:
        num -= 1
    yield num


def divide_images():
    chopped = chop_arrays_to_grids(block_length, processed)
    save_to_hf("data.h5", h5_data_folder, chopped)


def generate_random():
    grids = read_h5("data.h5", h5_data_folder)
    generated_image = create_image(img_height, img_width, grids, block_length)
    # generated_image = cv2.blur(generated_image, (10, 29))
    t = time.localtime()
    current_time = time.strftime("%d-%m-%Y_%H_%M_%S", t)
    image_save_location = os.path.join(output_imgs, current_time + ".jpg")
    cv2.imshow("CroppedImage", generated_image)  # Show Cropped Image
    cv2.waitKey(0)
    cv2.imwrite(image_save_location, generated_image)


def close():
    sys.exit()


commands = {
    "p": process_images,
    "d": divide_images,
    "r": generate_random,
    "exit": close
}


def main():
    running = True
    while running:
        print("Type Command: \np = process images\nd = divide blocks\nr = generate random image ")
        text = input().lower()
        try:
            commands[text]()
        except KeyError:
            print("Input error")


if __name__ == '__main__':
    main()
