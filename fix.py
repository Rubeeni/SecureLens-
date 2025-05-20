import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Load the trained model
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("securelens_model.h5", compile=False)
    return model

model = load_model()

st.title("SecureLens AI Moderation System")
st.write("Welcome to SecureLens! Upload an image to check its clothing coverage percentage.")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Preprocess the image for the model
    image = image.resize((224, 224))  # Resize to match model input size
    image_array = np.array(image) / 255.0  # Normalize pixel values
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

    # Make a prediction
    prediction = model.predict(image_array)
    
    # Assuming model output gives clothing percentage
    clothing_coverage = float(prediction[0][0]) * 100  # Convert to percentage

    # Display result
    st.write(f"👕 Clothing Coverage: **{clothing_coverage:.2f}%**")

    # Eligibility check
    if clothing_coverage < 20:
        st.error("🚫 This image is **NOT** eligible to post (Too much exposed skin).")
    elif clothing_coverage > 50:
        st.success("✅ This image is **eligible** to post.")
