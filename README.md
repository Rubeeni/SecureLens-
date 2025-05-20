# SecureLens – AI-Powered Image Moderation Web App

**SecureLens** is a web-based content moderation system designed to automatically analyze and filter uploaded images based on clothing coverage percentage. Using a MobileNetV2 model trained on a custom dataset, it intelligently determines whether an image is appropriate for posting.

---

## 🔍 Features
- 🔐 User authentication system (Login / Signup)
- 🧠 AI-based clothing coverage detection
- ❌ Blocks images with < 20% coverage
- ✅ Approves and posts eligible content
- 📸 Feed with caption, likes, comments, and emoji-based reactions
- ⏳ Session-based temporary post storage for demo purposes

---

## 📁 Project Files
| File Name     | Description                          |
|---------------|--------------------------------------|
| `final.py`    | ✨ Main Streamlit application file |
| `securelens_model.h5` | Trained MobileNetV2 AI model |
| `1.webp`      | Sample image for testing             |
| `acc.py`, `main.py`, `fix.py`, `new.py`, `scriptss.py` | Test/dev helper files |

---

## ⚙️ How to Run the App

### 1. Install dependencies:
```bash
pip install streamlit tensorflow pillow numpy
```

### 2. Run the Streamlit app:
```bash
streamlit run final.py
```

### 3. Use the app:
- Sign up or log in
- Upload an image
- See clothing percentage prediction
- Post eligible images to the feed

---

## 📈 Model Overview
- **Architecture**: MobileNetV2
- **Training Data**: ~1000 images
- **Achieved Accuracy**: 60.88%
- **Moderation Rule**: Blocks images with < 20% clothing coverage

---

## 🛡️ Ethical & Privacy Statement
- No permanent data or image storage is used
- All moderation is done in-session
- Project follows responsible AI principles

---

## 🌐 Demo Use Case
Ideal for demo purposes or prototype systems where content moderation is necessary but permanent backend storage is not required. This system can be extended with database integration and cloud storage.

---

Created with ❤ by **Rubeeni**
