# TEAM5 : Emotion Music System

🎵 **Emotion Music System** is a Python-based real-time system that recognizes a user's facial expression, classifies the emotion, and automatically plays music that matches that emotion.

---

# Member List and Roles

1. **m5281014, Yusei Ichikawa** – Presentation and system concept
2. **m5281030, NAKAMURA Zen** – System development
3. **m5291051, MURAKAMI Tatsuya** – Music selection
4. **m5291067, SHU Hoshitaka** – System development

---

## 🧠 System Overview

* The system captures the user's face using a laptop webcam
* The captured image is sent to a YOLO model running on Google Colab
* The YOLO model predicts one of four emotions:

  **Angry, Sad, Happy, or Neutral**
* Based on the predicted emotion, the local PC plays the corresponding music

---

## 🏗️ Project Structure

emotion-music-system/

├── fine-tune/                    # Folder for model fine-tuning
   ├── data.yaml
   └── train_command.txt         # YOLO training command

├── send_image_to_colab.py       # Sends webcam image to Colab for inference
├── play_music_by_emotion.py     # Plays music based on predicted emotion
├── emotion_music_config.json    # Maps emotion labels to music file paths
├── music/                       # Folder to store music files
├── .gitignore                   # Git ignore settings
└── README.md                    # This file


## ⚙️ Development Environment *(To be finalized)*

* Python 3.8+
* OpenCV (`cv2`)
* `requests`
* Flask (for the server on Colab)
* `pygame` (for local music playback)

---

## 🚀 Model Used

* [YOLOv5 / YOLOv8](https://github.com/ultralytics/yolov5), using a pre-trained model on Google Colab
* Emotion classification:  **Angry** ,  **Sad** ,  **Happy** , **Neutral** (4 classes)

  → Re-training only the final classification layer is sufficient

---

## 📊 Dataset

* **Facial Expression Image Data AFFECTNET YOLO Format**

  [https://www.kaggle.com/datasets/fatihkgg/affectnet-yolo-format](https://www.kaggle.com/datasets/fatihkgg/affectnet-yolo-format)

  * We use 4 emotion labels:
    * **Angry** ,  **Sad** ,  **Happy** , **Neutral**

---

## 🎯 Project Goal

To create a simple, intuitive system that reacts to a user's emotional expression and responds with appropriate background music in real time.
