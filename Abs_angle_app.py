import math
import random
import streamlit as st
import matplotlib.pyplot as plt

# Function to generate random coordinates
def generate_coordinates():
    GTX = round(random.uniform(-0.25, -0.19), 3)
    GTY = round(random.uniform(0.83, 0.98), 3)
    LEX = round(random.uniform(-0.15, -0.1), 3)
    LEY = round(random.uniform(0.48, 0.54), 3)
    LMX = round(random.uniform(-0.25, -0.15), 3)
    LMY = round(random.uniform(0.08, 0.12), 3)
    return GTX, GTY, LEX, LEY, LMX, LMY

# Function to calculate absolute angle between two points
def calculate_absolute_angle(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    angle_rad = math.atan2(delta_y, delta_x)
    angle_deg = math.degrees(angle_rad)
    if angle_deg < 0:
        angle_deg += 360
    return round(angle_deg, 1)

# Initialize session state if not already initialized
if 'GTX' not in st.session_state:
    st.session_state.GTX, st.session_state.GTY, st.session_state.LEX, st.session_state.LEY, st.session_state.LMX, st.session_state.LMY = generate_coordinates()
    st.session_state.thigh_angle = calculate_absolute_angle(st.session_state.GTX, st.session_state.GTY, st.session_state.LEX, st.session_state.LEY)
    st.session_state.leg_angle = calculate_absolute_angle(st.session_state.LEX, st.session_state.LEY, st.session_state.LMX, st.session_state.LMY)
    st.session_state.knee_angle = st.session_state.thigh_angle - st.session_state.leg_angle
    st.session_state.correct_answers = 0
    st.session_state.attempted_answers = 0

# Title
st.title("Absolute Thigh Angle, Leg Angle, and Knee Flexion Practice App")

# Display the Provided Coordinates
st.subheader("Provided Coordinates")

coords = {
    "Anatomical Location": ["Greater Trochanter", "Lateral Epicondyle", "Lateral Malleolus"],
    "X Position (m)": [st.session_state.GTX, st.session_state.LEX, st.session_state.LMX],
    "Y Position (m)": [st.session_state.GTY, st.session_state.LEY, st.session_state.LMY]
}

st.table(coords)

st.markdown("Assume the person is walking in the positive X direction.")

# Inputs for student's estimated angles
student_thigh_angle = st.number_input("Your estimated absolute thigh angle (degrees):", step=0.1, key='thigh')
student_leg_angle = st.number_input("Your estimated absolute leg (shank) angle (degrees):", step=0.1, key='leg')
student_knee_angle = st.number_input("Your estimated knee flexion angle (degrees):", step=0.1, key='knee')

# Buttons for individual checks
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Check Thigh Angle"):
        st.session_state.attempted_answers += 1
        if abs(student_thigh_angle - st.session_state.thigh_angle) <= 1.0:
            st.session_state.correct_answers += 1
            st.success(f"✅ Correct! The absolute thigh angle is {st.session_state.thigh_angle}°.")
        else:
            st.error(f"❌ Incorrect. The correct absolute thigh angle is {st.session_state.thigh_angle}°.")

with col2:
    if st.button("Check Leg Angle"):
        st.session_state.attempted_answers += 1
        if abs(student_leg_angle - st.session_state.leg_angle) <= 1.0:
            st.session_state.correct_answers += 1
            st.success(f"✅ Correct! The absolute leg angle is {st.session_state.leg_angle}°.")
        else:
            st.error(f"❌ Incorrect. The correct absolute leg angle is {st.session_state.leg_angle}°.")

with col3:
    if st.button("Check Knee Angle"):
        st.session_state.attempted_answers += 1
        if abs(student_knee_angle - st.session_state.knee_angle) <= 1.0:
            st.session_state.correct_answers += 1
            st.success(f"✅ Correct! The knee flexion angle is {st.session_state.knee_angle}°.")
        else:
            st.error(f"❌ Incorrect. The correct knee flexion angle is {st.session_state.knee_angle}°.")

with col4:
    if st.button("New Problem"):
        st.session_state.GTX, st.session_state.GTY, st.session_state.LEX, st.session_state.LEY, st.session_state.LMX, st.session_state.LMY = generate_coordinates()
        st.session_state.thigh_angle = calculate_absolute_angle(st.session_state.GTX, st.session_state.GTY, st.session_state.LEX, st.session_state.LEY)
        st.session_state.leg_angle = calculate_absolute_angle(st.session_state.LEX, st.session_state.LEY, st.session_state.LMX, st.session_state.LMY)
        st.session_state.knee_angle = st.session_state.thigh_angle - st.session_state.leg_angle
        st.experimental_rerun()

# Display score
st.markdown(f"**Score:** {st.session_state.correct_answers} correct out of {st.session_state.attempted_answers} attempts")

# Explanation Section
st.subheader("📚 How to Calculate:")
st.markdown("**Absolute Thigh Angle:**")
st.latex(r"\Delta x = LEX - GTX")
st.latex(r"\Delta y = LEY - GTY")
st.latex(r"\text{Absolute Thigh Angle} = \text{atan2}(\Delta y, \Delta x)")

st.markdown("**Absolute Leg (Shank) Angle:**")
st.latex(r"\Delta x = LMX - LEX")
st.latex(r"\Delta y = LMY - LEY")
st.latex(r"\text{Absolute Leg Angle} = \text{atan2}(\Delta y, \Delta x)")

st.markdown("**Knee Flexion Angle:**")
st.latex(r"\text{Knee Flexion Angle} = \text{Absolute Thigh Angle} - \text{Absolute Leg Angle}")

# Plot Section
st.subheader("📈 Plot of the Segment Coordinates:")
fig, ax = plt.subplots()
ax.plot([st.session_state.GTX, st.session_state.LEX], [st.session_state.GTY, st.session_state.LEY], 'bo-', label='Thigh (GT → LE)')
ax.plot([st.session_state.LEX, st.session_state.LMX], [st.session_state.LEY, st.session_state.LMY], 'go-', label='Leg (LE → LM)')

# Label points
ax.text(st.session_state.GTX, st.session_state.GTY, 'GT', fontsize=9, ha='right')
ax.text(st.session_state.LEX, st.session_state.LEY, 'LE', fontsize=9, ha='left')
ax.text(st.session_state.LMX, st.session_state.LMY, 'LM', fontsize=9, ha='left')

ax.set_xlabel('X Position (m)')
ax.set_ylabel('Y Position (m)')
ax.set_title('Thigh and Leg Segments')
ax.grid(True)
ax.legend()
st.pyplot(fig)
