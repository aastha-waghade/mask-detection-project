import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load model
model = load_model("model/mask_model.h5")

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

IMG_SIZE = 100
CONF_THRESHOLD = 0.7
DIFF_THRESHOLD = 0.25


def detect(frame):

    frame = cv2.resize(frame, (640, 480))

    # 🔥 FIX: reduce over-brightness
    frame = cv2.convertScaleAbs(frame, alpha=1.05, beta=5)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(40, 40)
)

    mask_count = 0
    no_mask_count = 0
    detected_boxes = []

    for (x, y, w, h) in faces:

        # 🔥 remove duplicate detections
        duplicate = False
        for (px, py, pw, ph) in detected_boxes:
            if abs(x - px) < 40 and abs(y - py) < 40:
                duplicate = True
                break

        if duplicate:
            continue

        detected_boxes.append((x, y, w, h))

        # 🔥 better face crop (IMPORTANT)
        padding = 20
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(frame.shape[1], x + w + padding)
        y2 = min(frame.shape[0], y + h + padding)

        face = frame[y1:y2, x1:x2]

        if face is None or face.size == 0:
            continue

        # preprocess
        face = cv2.resize(face, (IMG_SIZE, IMG_SIZE))
        face = face.astype("float32") / 255.0
        face = np.expand_dims(face, axis=0)

        # prediction
        pred = model.predict(face, verbose=0)[0]

        mask_prob = float(pred[0])
        no_mask_prob = float(pred[1])

        # 🔥 FINAL DECISION LOGIC
        # 🔥 balanced logic (BEST)

        if mask_prob > 0.55 and mask_prob > no_mask_prob:
         label = f"Mask {mask_prob*100:.0f}%"
         color = (0, 255, 0)
         mask_count += 1

        elif no_mask_prob > 0.55 and no_mask_prob > mask_prob:
         label = f"No Mask {no_mask_prob*100:.0f}%"
         color = (0, 0, 255)
         no_mask_count += 1

        else:
         label = "Detecting..."
         color = (255, 255, 0)

        # 🔥 draw box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2)

    # total count
    total = mask_count + no_mask_count

    cv2.putText(frame, f"Mask: {mask_count}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0), 2)

    cv2.putText(frame, f"No Mask: {no_mask_count}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255), 2)

    cv2.putText(frame, f"Total: {total}",
                (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255), 2)

    return frame, mask_count, no_mask_count