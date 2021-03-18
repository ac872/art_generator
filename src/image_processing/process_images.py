import cv2
import os
import unprocessed
import processed


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append([img, filename])  # Append image and image filename
    return images


def crop_images(images):
    # Cropped from top left of the image
    y = 0
    x = 0
    # Define size of cropped images
    h = 640
    w = 640
    for row in images:
        row[0] = row[0][x:w, y:h]
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
