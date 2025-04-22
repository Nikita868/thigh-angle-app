import math
import streamlit as st
import matplotlib.pyplot as plt

# Manual test case from the user
GTX, GTY = 0.119, 0.959
LEX, LEY = 0.275, 0.475
LMX, LMY = 0.082, 0.1

# Function to calculate absolute angle from proximal to distal
def calculate_absolute_angle(proximal_x, proximal_y, distal_x, distal_y):
    delta_x = proximal_x - distal_x
    delta_y = proximal_y - distal_y
    angle_rad = math.atan2(delta_y, delta_x)
    angle_deg = math.degrees(angle_rad)

    # Apply quadrant correction
    if delta_x > 0 and delta_y >= 0:  # Quadrant 1
        pass
    elif delta_x < 0:  # Quadrant 2 or 3
        angle_deg += 0
    elif delta_x > 0 and delta_y < 0:  # Quadrant 4
        angle_deg += 360

    return round(angle_deg, 1)

# Calculate angles
thigh_angle = calculate_absolute_angle(GTX, GTY, LEX, LEY)
leg_angle = calculate_absolute_angle(LEX, LEY, LMX, LMY)
knee_angle = round(thigh_angle - leg_angle, 1)

# Streamlit app layout
st.title("Debug: Absolute Angle Calculation")

st.subheader("Coordinates")
st.write("GT (Greater Trochanter):", (GTX, GTY))
st.write("LE (Lateral Epicondyle):", (LEX, LEY))
st.write("LM (Lateral Malleolus):", (LMX, LMY))

# Input for student's estimated angles
student_thigh_angle = st.number_input("Your estimated absolute thigh angle (degrees):", step=0.1, key='thigh')
student_leg_angle = st.number_input("Your estimated absolute leg (shank) angle (degrees):", step=0.1, key='leg')
student_knee_angle = st.number_input("Your estimated knee flexion angle (degrees):", step=0.1, key='knee')

# Buttons for checking answers
col1, col2, col3 = st.columns(3)

if 'knee_checked' not in st.session_state:
    st.session_state.knee_checked = False
if 'show_how' not in st.session_state:
    st.session_state.show_how = False

with col1:
    if st.button("Check Thigh Angle"):
        if abs(student_thigh_angle - thigh_angle) <= 0.1:
            st.success(f"✅ Correct! The absolute thigh angle is {thigh_angle:.1f}°.")
        else:
            st.error(f"❌ Incorrect. The correct absolute thigh angle is {thigh_angle:.1f}°.")

with col2:
    if st.button("Check Leg Angle"):
        if abs(student_leg_angle - leg_angle) <= 0.1:
            st.success(f"✅ Correct! The absolute leg angle is {leg_angle:.1f}°.")
        else:
            st.error(f"❌ Incorrect. The correct absolute leg angle is {leg_angle:.1f}°.")

with col3:
    if st.button("Check Knee Angle"):
        if abs(student_knee_angle - knee_angle) <= 0.1:
            st.success(f"✅ Correct! The knee flexion angle is {knee_angle:.1f}°.")
        else:
            st.error(f"❌ Incorrect. The correct knee flexion angle is {knee_angle:.1f}°.")
        st.session_state.knee_checked = True

# After knee checked, offer "Show How to Calculate" button
if st.session_state.knee_checked:
    if st.button("Show How to Calculate"):
        st.session_state.show_how = True

# Show explanation only after clicking Show How to Calculate
if st.session_state.show_how:
    st.subheader("📚 How to Calculate:")
    st.markdown("**Absolute Thigh Angle:**")
    st.latex(r"\Delta x = GTX - LEX")
    st.latex(r"\Delta y = GTY - LEY")
    st.latex(r"\text{Thigh Angle} = \text{atan2}(\Delta y, \Delta x)")
