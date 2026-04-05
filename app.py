import base64
import numpy as np
from flask import Flask, render_template, jsonify, request
import cv2, sqlite3, time
from datetime import datetime
from detect_mask import detect

app = Flask(__name__)

last_saved_time = {}
last_counts = {}
SAVE_INTERVAL = 2


# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("database/data.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        total_mask INTEGER,
        total_no_mask INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()


# ---------------- ROUTES ----------------
@app.route('/')
def home():
    return render_template("index.html")


# 🔥 FIXED ADMIN (single day data)
@app.route('/admin')
def admin():
    conn = sqlite3.connect("database/data.db")
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    data = c.execute("""
        SELECT date,
               SUM(total_mask),
               SUM(total_no_mask)
        FROM logs
        WHERE date = ?
    """, (today,)).fetchone()

    conn.close()

    return render_template("dashboard.html", data=data)


# ---------------- DETECTION ----------------
@app.route('/detect_frame', methods=['POST'])
def detect_frame():
    try:
        data = request.json['image']
        encoded = data.split(",")[1]

        img_bytes = base64.b64decode(encoded)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        frame = cv2.resize(frame, (640, 480))

        frame, mask, no_mask = detect(frame)

        total_faces = mask + no_mask

        current_time = time.time()
        allow_update = True

        # 🔥 FIXED TIME CONTROL
        if "global" in last_saved_time:
            if current_time - last_saved_time["global"] < SAVE_INTERVAL:
                allow_update = False

        prev_count = last_counts.get("global", -1)

        if allow_update and total_faces != prev_count:

            conn = sqlite3.connect("database/data.db")
            c = conn.cursor()

            today = datetime.now().strftime("%Y-%m-%d")

            c.execute("SELECT id FROM logs WHERE date=?", (today,))
            row = c.fetchone()

            if row:
                log_id = row[0]

                c.execute("""
                    UPDATE logs
                    SET total_mask = total_mask + ?,
                        total_no_mask = total_no_mask + ?
                    WHERE id = ?
                """, (mask, no_mask, log_id))

            else:
                c.execute("""
                    INSERT INTO logs (date, total_mask, total_no_mask)
                    VALUES (?, ?, ?)
                """, (today, mask, no_mask))

            conn.commit()
            conn.close()

            last_saved_time["global"] = current_time
            last_counts["global"] = total_faces

        # 🔥 SEND IMAGE BACK
        _, buffer = cv2.imencode('.jpg', frame)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        return jsonify({
            "mask": int(mask),
            "no_mask": int(no_mask),
            "image": img_base64
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Detection failed"})


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)