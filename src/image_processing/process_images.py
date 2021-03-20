import cv2
import h5py
import os
import unprocessed
import processed


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
    block_length = 10
    # Ensure image size is multiple of 10
    for row in images:
        image = row[0]
        h, w, z = image.shape  # discard z
        h = next(is_multiple_of(h, block_length))
        w = next(is_multiple_of(w, block_length))
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


def image_crop():
    raw_img_filepath = os.path.dirname(unprocessed.__file__)
    raw_imgs = load_images_from_folder(raw_img_filepath)
    processed_imgs = crop_images(raw_imgs)
    processed_img_filepath = os.path.dirname(processed.__file__)
    save_images(processed_imgs, processed_img_filepath)


def is_multiple_of(num, multiple=10):
    while not num % multiple == 0:
        num -= 1
    yield num


