import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Load the trained model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("securelens_model.h5", compile=False)

model = load_model()

# Define class labels
class_labels = ["NSFW", "SFW"]

def predict_image(image):
    image = image.resize((224, 224))  # Resize for model
    image_array = np.array(image) / 255.0  # Normalize
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dim
    prediction = model.predict(image_array)[0]  # Get prediction probabilities
    return prediction

st.title("SecureLens - Image Moderation System")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    prediction = predict_image(image)
    
    # Ensure correct indexing
    nsfw_score = prediction[0] * 100  # NSFW Score
    sfw_score = prediction[1] * 100 if len(prediction) > 1 else 100 - nsfw_score  # SFW Score
    
    # Display Confidence Scores
    st.write(f"NSFW Confidence: {nsfw_score:.2f}%")
    st.write(f"SFW Confidence: {sfw_score:.2f}%")
    
    # Determine Clothing Coverage (Using SFW Score)
    clothing_coverage = sfw_score  # Assuming SFW score represents clothing coverage
    st.write(f"Clothing Coverage: {clothing_coverage:.2f}%")

    # Decision Logic
    if clothing_coverage >= 10:  # Allow if clothing coverage is 10% or more
        st.success("✅ The photo is eligible to post.")
        if st.button("Post Image"):
            st.write("✔ Image successfully posted!")
    else:
        st.error("❌ The photo is not eligible to post.")

    # Debugging Output
    st.write("Raw Model Prediction:", prediction)

    # Threshold Logic (Move Inside the Condition)
    THRESHOLD = 80  # Allow images below 80% NSFW score
    if nsfw_score < THRESHOLD:
        st.success("✅ The photo is eligible to post.")
    else:
        st.error("❌ The photo is not eligible to post.")

else:
    st.warning("⚠ Please upload an image first!")
