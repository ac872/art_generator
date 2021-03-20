from image_processing.process_images import load_images_from_folder
import processed
import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout


images = load_images_from_folder(os.path.dirname(processed.__file__))
images = [i[0] for i in images]  # Remove filenames
images = [i / 255 for i in images]  # Ratio numbers to 255:0 so can be used for ML
array_shape = images[0].shape

model = Sequential()
model.add(Conv2D(filters=16, kernel_size=2, padding="same", activation="relu", input_shape=array_shape))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=32, kernel_size=2, padding="same", activation="tanh"))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=64, kernel_size=2, padding="same", activation="tanh"))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(500, activation="relu"))
model.add(Dropout(0.4))
model.add(Dense(2, activation="softmax"))

model.summary()

model.compile(loss="catergorical_crossentropy", optimizer="rmsprop")

history = model.fit()
