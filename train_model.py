import os
import numpy as np
import cv2
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

print("Loading dataset...")

data = []
labels = []

categories = ["with_mask", "without_mask"]

for category in categories:
    path = os.path.join("dataset", category)
    label = categories.index(category)

    for img in os.listdir(path):
        try:
            img_path = os.path.join(path, img)
            image = cv2.imread(img_path)

            if image is None:
                continue

            image = cv2.resize(image, (100, 100))
            data.append(image)
            labels.append(label)

        except:
            continue

print("Dataset Loaded ✅")

data = np.array(data) / 255.0
labels = to_categorical(labels)

print("Training model...")

model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(100,100,3)),
    MaxPooling2D(),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(2, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(data, labels, epochs=5)

model.save("model/mask_model.h5")

print("MODEL TRAINED SUCCESSFULLY 🎉")