Here’s a polished **README.md** draft for your Flask‑based Mask Detection project:

```markdown
# 😷 Face Mask Detection System

A real‑time web application built with **Flask, OpenCV, and SQLite** to detect whether people are wearing masks.  
The system logs detection results, provides an admin dashboard, and supports live monitoring.

---

## 🚀 Features

- **Real‑time Detection**  
  Detects faces with/without masks from video frames.

- **Database Logging**  
  Stores daily counts of mask vs. no‑mask detections in SQLite.

- **Admin Dashboard**  
  Displays aggregated statistics for the current day.

- **Time‑Controlled Logging**  
  Prevents duplicate entries by enforcing a save interval.

- **REST API Endpoint**  
  `/detect_frame` accepts base64‑encoded images and returns detection results with the processed frame.

---

## 📂 Project Structure

```
├── app.py              # Main Flask application
├── detect_mask.py      # Detection logic (mask vs. no mask)
├── train_model.py      # Model training script
├── static/             # Static assets (CSS, JS)
├── templates/          # HTML templates (index, dashboard)
├── database/           # SQLite database folder
└── README.md           # Documentation
```

---

## ⚙️ Technologies Used

- **Backend**: Flask (Python)  
- **Computer Vision**: OpenCV  
- **Database**: SQLite  
- **Frontend**: HTML, CSS, JavaScript (templates)  
- **Data Handling**: NumPy, Base64  

---

## 🛠️ Setup & Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mask-detection.git
   cd mask-detection
   ```

2. Install dependencies:
   ```bash
   pip install flask opencv-python numpy
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open in browser:
   ```
   http://127.0.0.1:5000/
   ```

---

## 🔑 API Endpoints

- **`/`** → Home page  
- **`/admin`** → Admin dashboard (daily stats)  
- **`/detect_frame` [POST]** → Accepts JSON with base64 image, returns detection results and processed frame  

Example request:
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA..."
}
```

Example response:
```json
{
  "mask": 3,
  "no_mask": 1,
  "image": "<base64 encoded processed frame>"
}
```

---

## 📊 Database Schema

Table: **logs**
- `id` → Primary key  
- `date` → Date of log (YYYY‑MM‑DD)  
- `total_mask` → Count of detected masked faces  
- `total_no_mask` → Count of detected unmasked faces  

---

## 📈 Future Enhancements

- Multi‑day analytics dashboard  
- Role‑based authentication for admins  
- Integration with cloud databases (PostgreSQL, MySQL)  
- Real‑time video stream detection  
- Email/SMS alerts for violations  

---

## 📜 License

This project is licensed under the MIT License.  
Feel free to use and modify it for your own needs.

---

## 👩‍💻 Author

Developed by **Aastha Waghade**  
📍 Nagpur, India  
```

