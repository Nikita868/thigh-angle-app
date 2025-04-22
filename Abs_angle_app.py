import math
import random
import streamlit as st

# Function to generate random coordinates
def generate_coordinates():
    GTX = round(random.uniform(-0.25, -0.19), 3)
    GTY = round(random.uniform(0.83, 0.98), 3)
    LEX = round(random.uniform(-0.15, -0.1), 3)
    LEY = round(random.uniform(0.48, 0.54), 3)
    LMX = round(random.uniform(-0.25, -0.15), 3)
    LMY = round(random.uniform(0.08, 0.12), 3)
    return GTX, GTY, LEX, LEY, LMX, LMY

# Function to calculate absolute thigh angle
def calculate_absolute_angle(GTX, GTY, LEX, LEY):
    delta_x = LEX - GTX
    delta_y = LEY - GTY
    angle_rad = math.atan2(delta_y, delta_x)
    angle_deg = math.degrees(angle_rad)
    if angle_deg < 0:
        angle_deg += 360
    return round(angle_deg, 1)

# Initialize session state if not already initialized
if 'GTX' not in st.session_state:
    st.session_state.GTX, st.session_state.GTY, st.session_state.LEX, st.session_state.LEY, st.session_state.LMX, st.session_state.LMY = generate_coordinates()
    st.session_state.true_thigh_angle = calculate_absolute_angle(st.session_state.GTX, st.session_state.GTY, st.session_state.LEX, st.session_state.LEY)
    st.session_state.correct_answers = 0
    st.session_state.attempted_answers = 0

# Title
st.title("Absolute Thigh Angle Practice App")

# Display the Provided Coordinates
st.subheader("Provided Coordinates")

coords = {
    "Anatomical Location": ["Greater Trochanter", "Lateral Epicondyle", "Lateral Malleolus"],
    "X Position (m)": [st.session_state.GTX, st.session_state.LEX, st.session_state.LMX],
    "Y Position (m)": [st.session_state.GTY, st.session_state.LEY, st.session_state.LMY]
}

st.table(coords)

st.markdown("Assume the person is walking in the positive X direction. Estimate the **absolute angle** of the **thigh segment**. Report your answer in **degrees to one decimal place**.")

# Input for student's estimated angle
student_angle = st.number_input("Your estimated angle (degrees):", step=0.1)

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Check Answer"):
        st.session_state.attempted_answers += 1
        if abs(student_angle - st.session_state.true_thigh_angle) <= 1.0:
            st.session_state.correct_answers += 1
            st.success(f"✅ Correct! The absolute thigh angle is {st.session_state.true_thigh_angle}°.")
        else:
            st.error(f"❌ Not quite. The correct absolute thigh angle is {st.session_state.true_thigh_angle}°. Try again!")

with col2:
    if st.button("New Problem"):
        st.session_state.GTX, st.session_state.GTY, st.session_state.LEX, st.session_state.LEY, st.session_state.LMX, st.session_state.LMY = generate_coordinates()
        st.session_state.true_thigh_angle = calculate_absolute_angle(st.session_state.GTX, st.session_state.GTY, st.session_state.LEX, st.session_state.LEY)
        st.experimental_rerun()

# Display score
st.markdown(f"**Score:** {st.session_state.correct_answers} correct out of {st.session_state.attempted_answers} attempts")
