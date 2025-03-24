import streamlit as sl
from datetime import datetime as datetime
import os
import time
from PIL import Image
from dateutil.relativedelta import relativedelta

# Define constants
START_DATE = datetime(2024, 12, 14)
END_DATE = datetime(2025, 12, 14)
AVATAR1_PATH = "Avatar1.png"
AVATAR2_PATH = "Avatar2.png"

ImageFile.LOAD_TRUNCATED_IMAGES = True

sl.set_page_config(layout="wide")
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

# Layout for avatars and progress
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
        sl.image(right_avatar, width=200 , caption="Avatar 2")
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

# Progress bar and time display
with progress_col:
    time_display = sl.empty()
    progress_bar = sl.progress(0)
    percentage_display = sl.empty()

current_time = datetime.now()
time_diff = END_DATE - current_time
elapsed_seconds = (current_time - START_DATE).total_seconds()

if current_time < END_DATE:
    progress = min((elapsed_seconds / sl.session_state.total_seconds) * 100, 100)
    rd = relativedelta(END_DATE, current_time)

    time_text = f"""
    **Months Remaining:** {rd.months + (rd.years * 12)}\n
    **Days:** {rd.days}\n
    **Hours:** {rd.hours}\n
    **Minutes:** {rd.minutes}\n
    **Seconds:** {rd.seconds}
    """
    percentage_text = f"Finish your journey: {int(progress)}%"

else:
    progress = 100
    time_text = "Countdown Complete!"

time_display.markdown(time_text)
progress_bar.progress(int(progress))
percentage_display.markdown(f"**{percentage_text}**")


time.sleep(0.5)
sl.rerun()
