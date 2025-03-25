import streamlit as sl
from datetime import datetime as datetime
import os
import time
from PIL import Image
from dateutil.relativedelta import relativedelta

# Set wide layout to reduce blank space on sides
sl.set_page_config(layout="wide")

# Define constants
START_DATE = datetime(2024, 12, 14)
END_DATE = datetime(2025, 12, 14)
AVATAR1_PATH = "Avatar1.png"
AVATAR2_PATH = "Avatar2.png"

# CSS Styling for Background Image, Custom Font, and Enhanced Progress Bar
sl.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

    /* Set background image */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxE9USFkNZZq3jgQV4XvDDLHV9StOFCuQoph2BNQTnOI9l0rNYcogjBbM2HXUFTeC7Bks&usqp=CAU");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    /* Style the text */
    .center-text {
        text-align: center;
        font-size: 55px;
        line-height: 1.6;
        font-family: 'Pacifico', cursive;
    
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }

    
    # /* Style the progress bar */
    # .stProgress > div > div {
    #     height: 40px !important;
    # }
    # .stProgress > div > div > div {
    #     background-color: #FF69B4 !important;
    # }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if 'remaining' not in sl.session_state:
    sl.session_state.remaining = relativedelta(END_DATE, START_DATE)
if 'progress' not in sl.session_state:
    total_seconds = (END_DATE - START_DATE).total_seconds()
    sl.session_state.total_seconds = total_seconds

# Check if avatars exist
left_avatar = None
right_avatar = None
if os.path.exists(AVATAR1_PATH):
    left_avatar = Image.open(AVATAR1_PATH)
if os.path.exists(AVATAR2_PATH):
    right_avatar = Image.open(AVATAR2_PATH)

# Layout for avatars and progress bar with centered images
avatar_col, progress_col, avatar_col2 = sl.columns([1, 5, 1])

with avatar_col:
    if left_avatar:
        sl.image(left_avatar, width=200, caption="Avatar 1")
    else:
        sl.text("Avatar 1")
        left_upload = sl.file_uploader("Upload Avatar 1", type=["png", "jpg"], key="left_upload")
        if left_upload:
            left_avatar = Image.open(left_upload)
            left_avatar.save(AVATAR1_PATH)
            sl.rerun()

with avatar_col2:
    if right_avatar:
        sl.image(right_avatar, width=200, caption="Avatar 2")
    else:
        sl.text("Avatar 2")
        right_upload = sl.file_uploader("Upload Avatar 2", type=["png", "jpg"], key="right_upload")
        if right_upload:
            right_avatar = Image.open(right_upload)
            right_avatar.save(AVATAR2_PATH)
            sl.rerun()

# Allow selection of avatars to replace
selected_avatar = sl.radio("Select Avatar to Replace:", ["None", "Avatar 1", "Avatar 2"])

if selected_avatar == "Avatar 1" and left_avatar:
    new_avatar = sl.file_uploader("Upload new Avatar 1", type=["png", "jpg"], key="new_left_upload")
    if new_avatar:
        # Replace old image with new one
        os.remove(AVATAR1_PATH)  # Remove old file
        new_image = Image.open(new_avatar)
        new_image.save(AVATAR1_PATH)  # Save new file
        sl.success("Avatar 1 replaced successfully!")
        sl.rerun()

elif selected_avatar == "Avatar 2" and right_avatar:
    new_avatar = sl.file_uploader("Upload new Avatar 2", type=["png", "jpg"], key="new_right_upload")
    if new_avatar:
        # Replace old image with new one
        os.remove(AVATAR2_PATH)  # Remove old file
        new_image = Image.open(new_avatar)
        new_image.save(AVATAR2_PATH)  # Save new file
        sl.success("Avatar 2 replaced successfully!")
        sl.rerun()

# Progress bar and time display in the center column
with progress_col:
    current_time = datetime.now()
    time_diff = END_DATE - current_time
    elapsed_seconds = (current_time - START_DATE).total_seconds()

    if current_time < END_DATE:
        progress = min((elapsed_seconds / sl.session_state.total_seconds) * 100, 100)
        rd = relativedelta(END_DATE, current_time)

        time_text = f"""
        <div class="center-text">
            <p><b>Months Remaining:</b> {rd.months + (rd.years * 12)}</p>
            <p><b>Days:</b> {rd.days}</p>
            <p><b>Hours:</b> {rd.hours}</p>
            <p><b>Minutes:</b> {rd.minutes}</p>
            <p><b>Seconds:</b> {rd.seconds}</p>
        </div>
        """
        percentage_text = f"<div class='center-text'><b>Finish your journey: {int(progress)}%</b></div>"
    else:
        progress = 100
        time_text = '<div class="center-text"><h3>Countdown Complete!</h3></div>'

    # Display countdown and progress bar
    sl.markdown(time_text, unsafe_allow_html=True)
    progress_bar = sl.progress(int(progress))
    sl.markdown(percentage_text, unsafe_allow_html=True)

time.sleep(0.5)
sl.rerun()
