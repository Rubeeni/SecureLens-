import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import datetime

# Dummy user database (Replace with actual DB in production)
USER_DATABASE = {
    "gokulaeswari": {"password": "1234", "posts": []},
    "user1": {"password": "0000", "posts": []},
}

# Load the trained AI model
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("securelens_model.h5", compile=False)
    return model

model = load_model()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["posts"] = []

# Authentication (Login & Sign Up)
def login():
    col1, col2 = st.columns([1, 1])
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    with col1:
        if st.button("Login"):
            if username in USER_DATABASE and USER_DATABASE[username]["password"] == password:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["posts"] = USER_DATABASE[username]["posts"]
                st.success(f"✅ Welcome, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password!")

    with col2:
        if st.button("Sign Up"):
            if username in USER_DATABASE:
                st.warning("⚠ Username already exists! Try a different one.")
            else:
                USER_DATABASE[username] = {"password": password, "posts": []}
                st.success("✅ Account created! You can now log in.")

if not st.session_state["logged_in"]:
    st.title("🔑 SecureLens Login")
    login()
else:
    st.sidebar.title(f"👤 Welcome, {st.session_state['username']}")
    menu = st.sidebar.radio("Navigation", ["Home", "Upload & Post", "Profile", "Logout"])

    if menu == "Logout":
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.session_state["posts"] = []
        st.rerun()

    elif menu == "Upload & Post":
        st.header("📤 Upload & Post an Image")

        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
        caption = st.text_area("Add a caption (optional)")

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            image = image.resize((224, 224))
            image_array = np.array(image) / 255.0
            image_array = np.expand_dims(image_array, axis=0)

            prediction = model.predict(image_array)
            clothing_coverage = float(prediction[0][0]) * 100

            st.write(f"👕 Clothing Coverage: **{clothing_coverage:.2f}%**")

            if clothing_coverage < 20:
                st.error("🚫 This image is **NOT** eligible to post.")
            else:
                st.success("✅ This image is **eligible** to post.")
                if st.button("📤 Post"):
                    post = {
                        "username": st.session_state["username"],
                        "image": uploaded_file,
                        "caption": caption,
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "likes": 0,
                        "comments": [],
                        "reactions": {"❤️": 0, "😂": 0, "😲": 0, "😢": 0, "😡": 0},
                    }
                    st.session_state["posts"].append(post)
                    USER_DATABASE[st.session_state["username"]]["posts"].append(post)
                    st.success("✅ Successfully posted!")
                    st.rerun()

    elif menu == "Home":
        st.header("🏠 Home Feed")

        if st.session_state["posts"]:
            for index, post in enumerate(reversed(st.session_state["posts"])):
                st.subheader(f"📌 {post['username']} posted at {post['timestamp']}")
                st.image(post["image"], use_column_width=True)
                st.write(f"{post['caption']}")
                st.write(f"👍 **Likes:** {post['likes']}")

                col1, col2, col3, col4, col5, col6 = st.columns(6)
                with col1:
                    if st.button(f"👍 {post['likes']}", key=f"like_{index}"):
                        post["likes"] += 1
                        st.rerun()
                with col2:
                    if st.button(f"❤️ {post['reactions']['❤️']}", key=f"heart_{index}"):
                        post["reactions"]["❤️"] += 1
                        st.rerun()
                with col3:
                    if st.button(f"😂 {post['reactions']['😂']}", key=f"laugh_{index}"):
                        post["reactions"]["😂"] += 1
                        st.rerun()
                with col4:
                    if st.button(f"😲 {post['reactions']['😲']}", key=f"wow_{index}"):
                        post["reactions"]["😲"] += 1
                        st.rerun()
                with col5:
                    if st.button(f"😢 {post['reactions']['😢']}", key=f"sad_{index}"):
                        post["reactions"]["😢"] += 1
                        st.rerun()
                with col6:
                    if st.button(f"😡 {post['reactions']['😡']}", key=f"angry_{index}"):
                        post["reactions"]["😡"] += 1
                        st.rerun()

                comment = st.text_input(f"💬 Add a comment:", key=f"comment_{index}")
                if st.button("Post Comment", key=f"post_comment_{index}"):
                    if comment:
                        post["comments"].append(comment)
                        st.success("✅ Comment added!")
                        st.rerun()

                if post["comments"]:
                    st.write("💬 **Comments:**")
                    for c in post["comments"]:
                        st.write(f"- {c}")

                st.markdown("---")
        else:
            st.write("No posts yet. Upload and post an image first! 👆")

    elif menu == "Profile":
        st.header(f"👤 {st.session_state['username']}'s Profile")

        if st.session_state["posts"]:
            for index, post in reversed(list(enumerate(st.session_state["posts"]))):
                st.subheader(f"📌 Posted on {post['timestamp']}")
                st.image(post["image"], use_column_width=True)
                st.write(f"📝 **Caption:** {post['caption']}")
                st.write(f"👍 **Likes:** {post['likes']}")

                col1, col2, col3, col4, col5, col6 = st.columns(6)
                with col1:
                    if st.button(f"👍 {post['likes']}", key=f"profile_like_{index}"):
                        post["likes"] += 1
                        st.rerun()
                with col2:
                    if st.button(f"❤️ {post['reactions']['❤️']}", key=f"profile_heart_{index}"):
                        post["reactions"]["❤️"] += 1
                        st.rerun()
                with col3:
                    if st.button(f"😂 {post['reactions']['😂']}", key=f"profile_laugh_{index}"):
                        post["reactions"]["😂"] += 1
                        st.rerun()
                with col4:
                    if st.button(f"😲 {post['reactions']['😲']}", key=f"profile_wow_{index}"):
                        post["reactions"]["😲"] += 1
                        st.rerun()
                with col5:
                    if st.button(f"😢 {post['reactions']['😢']}", key=f"profile_sad_{index}"):
                        post["reactions"]["😢"] += 1
                        st.rerun()
                with col6:
                    if st.button(f"😡 {post['reactions']['😡']}", key=f"profile_angry_{index}"):
                        post["reactions"]["😡"] += 1
                        st.rerun()

                comment = st.text_input(f"💬 Add a comment:", key=f"profile_comment_{index}")
                if st.button("Post Comment", key=f"profile_post_comment_{index}"):
                    if comment:
                        post["comments"].append(comment)
                        st.success("✅ Comment added!")
                        st.rerun()

                if post["comments"]:
                    st.write("💬 **Comments:**")
                    for c in post["comments"]:
                        st.write(f"- {c}")

                st.markdown("---")
        else:
            st.write("You haven't posted anything yet.")
