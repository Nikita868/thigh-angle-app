import math
import random
import streamlit as st
import matplotlib.pyplot as plt

# Function to generate realistic walking coordinates
def generate_coordinates():
    GTX = round(random.uniform(-0.20, -0.18), 3)  # GT slightly behind
    GTY = round(random.uniform(0.90, 0.98), 3)
    LEX = round(GTX + random.uniform(0.05, 0.07), 3)  # LE ahead of GT
    LEY = round(random.uniform(0.45, 0.52), 3)  # lower Y
    LMX = round(LEX + random.uniform(0.05, 0.08), 3)  # foot ahead of knee
    LMY = round(random.uniform(0.08, 0.12), 3)  # lowest point
    return GTX, GTY, LEX, LEY, LMX, LMY

# Function to calculate absolute angle from proximal to distal
def calculate_absolute_angle(proximal_x, proximal_y, distal_x, distal_y):
    delta_x = proximal_x - distal_x
    delta_y = proximal_y - distal_y
    angle_rad = math.atan2(delta_y, delta_x)
    angle_deg = math.degrees(angle_rad)

    if delta_x > 0 and delta_y >= 0:  # Quadrant 1
        pass
    elif delta_x < 0:  # Quadrant 2 or 3
        angle_deg += 180
    elif delta_x > 0 and delta_y < 0:  # Quadrant 4
        angle_deg += 360

    return round(angle_deg, 1)

# Initialize session state
if 'GTX' not in st.session_state:
    st.session_state.GTX, st.session_state.GTY, st.session_state.LEX, st.session_state.LEY, st.session_state.LMX, st.session_state.LMY = generate_coordinates()
    st.session_state.thigh_angle = calculate_absolute_angle(st.session_state.GTX, st.session_state.GTY, st.session_state.LEX, st.session_state.LEY)
    st.session_state.leg_angle = calculate_absolute_angle(st.session_state.LEX, st.session_state.LEY, st.session_state.LMX, st.session_state.LMY)
    st.session_state.knee_angle = round(st.session_state.thigh_angle - st.session_state.leg_angle, 1)
    st.session_state.correct_answers = 0
    st.session_state.attempted_answers = 0

st.title("Absolute Thigh Angle, Leg Angle, and Knee Flexion Practice App")

st.subheader("Problem Statement")
st.markdown("""
The data below is (x,y) position coordinates of a person walking. Use the data table provided below to estimate the absolute angle of the thigh segment. Assume they are walking in the positive X direction. Report in degrees to one decimal place.
""")

# Show coordinates
st.subheader("Provided Coordinates")
st.table({
    "Anatomical Location": ["Greater Trochanter", "Lateral Epicondyle", "Lateral Malleolus"],
    "X Position (m)": [st.session_state.GTX, st.session_state.LEX, st.session_state.LMX],
    "Y Position (m)": [st.session_state.GTY, st.session_state.LEY, st.session_state.LMY]
})

# Inputs
student_thigh_angle = st.number_input("Your estimated absolute thigh angle (degrees):", step=0.1, key='thigh')
student_leg_angle = st.number_input("Your estimated absolute leg (shank) angle (degrees):", step=0.1, key='leg')
student_knee_angle = st.number_input("Your estimated knee flexion angle (degrees):", step=0.1, key='knee')

# Buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Check Thigh Angle"):
        st.session_state.attempted_answers += 1
        if abs(student_thigh_angle - st.session_state.thigh_angle) <= 0.1:
            st.session_state.correct_answers += 1
            st.success(f"✅ Correct! The absolute thigh angle is {st.session_state.thigh_angle:.1f}°.")
        else:
            st.error(f"❌ Incorrect. The correct absolute thigh angle is {st.session_state.thigh_angle:.1f}°.")

with col2:
    if st.button("Check Leg Angle"):
        st.session_state.attempted_answers += 1
        if abs(student_leg_angle - st.session_state.leg_angle) <= 0.1:
            st.session_state.correct_answers += 1
            st.success(f"✅ Correct! The absolute leg angle is {st.session_state.leg_angle:.1f}°.")
        else:
            st.error(f"❌ Incorrect. The correct absolute leg angle is {st.session_state.leg_angle:.1f}°.")

with col3:
    if st.button("Check Knee Angle"):
        st.session_state.attempted_answers += 1
        if abs(student_knee_angle - st.session_state.knee_angle) <= 0.1:
            st.session_state.correct_answers += 1
            st.success(f"✅ Correct! The knee flexion angle is {st.session_state.knee_angle:.1f}°.")
        else:
            st.error(f"❌ Incorrect. The correct knee flexion angle is {st.session_state.knee_angle:.1f}°.")

with col4:
    if st.button("New Problem"):
        st.session_state.GTX, st.session_state.GTY, st.session_state.LEX, st.session_state.LEY, st.session_state.LMX, st.session_state.LMY = generate_coordinates()
        st.session_state.thigh_angle = calculate_absolute_angle(st.session_state.GTX, st.session_state.GTY, st.session_state.LEX, st.session_state.LEY)
        st.session_state.leg_angle = calculate_absolute_angle(st.session_state.LEX, st.session_state.LEY, st.session_state.LMX, st.session_state.LMY)
        st.session_state.knee_angle = round(st.session_state.thigh_angle - st.session_state.leg_angle, 1)
        st.experimental_rerun()

# Score
st.markdown(f"**Score:** {st.session_state.correct_answers} correct out of {st.session_state.attempted_answers} attempts")

# Explanation
st.subheader("📚 How to Calculate:")
st.markdown("**Absolute Thigh Angle:**")
st.latex(r"\Delta x = GTX - LEX")
st.latex(r"\Delta y = GTY - LEY")
st.latex(r"\text{Thigh Angle} = \text{atan2}(\Delta y, \Delta x)")
st.markdown("Apply quadrant correction:")
st.markdown("- Quadrant 1: Δx > 0, Δy > 0 → no correction")
st.markdown("- Quadrant 2/3: Δx < 0 → add 180°")
st.markdown("- Quadrant 4: Δx > 0, Δy < 0 → add 360°")

st.markdown("**Absolute Leg Angle:**")
st.latex(r"\Delta x = LEX - LMX")
st.latex(r"\Delta y = LEY - LMY")
st.latex(r"\text{Leg Angle} = \text{atan2}(\Delta y, \Delta x)")
st.markdown("(Apply same correction rules.)")

st.markdown("**Knee Flexion Angle:**")
st.latex(r"\text{Knee Angle} = \text{Thigh Angle} - \text{Leg Angle}")

# Plot
st.subheader("📈 Segment Plot")
fig, ax = plt.subplots()
ax.plot([st.session_state.GTX, st.session_state.LEX], [st.session_state.GTY, st.session_state.LEY], 'bo-', label='Thigh (GT → LE)')
ax.plot([st.session_state.LEX, st.session_state.LMX], [st.session_state.LEY, st.session_state.LMY], 'go-', label='Leg (LE → LM)')
ax.text(st.session_state.GTX, st.session_state.GTY, 'GT', fontsize=9, ha='right')
ax.text(st.session_state.LEX, st.session_state.LEY, 'LE', fontsize=9, ha='left')
ax.text(st.session_state.LMX, st.session_state.LMY, 'LM', fontsize=9, ha='left')
ax.set_xlabel('X Position (m)')
ax.set_ylabel('Y Position (m)')
ax.set_title('Thigh and Leg Segments')
ax.grid(True)
ax.legend()
st.pyplot(fig)
