import os
import streamlit as st
from datetime import datetime
import random

# Ensure the 'temp_images' directory exists
if not os.path.exists("temp_images"):
    os.makedirs("temp_images")

# Initialize posts if not present
if "posts" not in st.session_state:
    st.session_state.posts = []

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])
if uploaded_file is not None:
    image_path = f"temp_images/{uploaded_file.name}"
    
    # Save the uploaded image
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Add post details
    st.session_state.posts.append({
        "image": image_path,
        "timestamp": datetime.now(),
        "likes": random.randint(0, 100),
        "comments": []
    })
    st.success("✅ Image uploaded successfully!")

# Display posts
st.write("### Uploaded Images:")
for post in st.session_state.posts:
    st.image(post["image"], use_column_width=True)
