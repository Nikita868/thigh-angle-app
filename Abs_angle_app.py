import math
import random
import ipywidgets as widgets
from IPython.display import display, Markdown

# Generate random coordinates based on given ranges
def generate_coordinates():
    GTX = round(random.uniform(-0.25, -0.19), 3)
    GTY = round(random.uniform(0.83, 0.98), 3)
    LEX = round(random.uniform(-0.15, -0.1), 3)
    LEY = round(random.uniform(0.48, 0.54), 3)
    LMX = round(random.uniform(-0.25, -0.15), 3)
    LMY = round(random.uniform(0.08, 0.12), 3)
    return GTX, GTY, LEX, LEY, LMX, LMY

# Calculate absolute angle of the thigh (GT to LE)
def calculate_absolute_angle(GTX, GTY, LEX, LEY):
    delta_x = LEX - GTX
    delta_y = LEY - GTY
    angle_rad = math.atan2(delta_y, delta_x)
    angle_deg = math.degrees(angle_rad)
    if angle_deg < 0:
        angle_deg += 360
    return round(angle_deg, 1)

# Initialize widgets
check_button = widgets.Button(description='Check Answer')
new_problem_button = widgets.Button(description='New Problem')
output = widgets.Output()
score_output = widgets.Output()
student_angle_input = widgets.FloatText(description='Your Angle (°):', step=0.1)

# Initialize problem and score
GTX, GTY, LEX, LEY, LMX, LMY = generate_coordinates()
true_thigh_angle = calculate_absolute_angle(GTX, GTY, LEX, LEY)
correct_answers = 0
attempted_answers = 0

# Function to update displayed coordinates
def display_coordinates():
    output.clear_output()
    with output:
        display(Markdown(f"""
### Provided Coordinates
| Anatomical Location | X Position (m) | Y Position (m) |
|:--------------------|:--------------:|:--------------:|
| Greater Trochanter  | {GTX} | {GTY} |
| Lateral Epicondyle  | {LEX} | {LEY} |
| Lateral Malleolus   | {LMX} | {LMY} |

Assume the person is walking in the positive X direction.
Estimate the **absolute angle** of the **thigh segment**.
Report your answer in **degrees to one decimal place**.
"""))
        display(student_angle_input, check_button, new_problem_button)

# Function to update score
def update_score_display():
    score_output.clear_output()
    with score_output:
        display(Markdown(f"**Score:** {correct_answers} correct out of {attempted_answers} attempts"))

# Callback to check answer
def on_check_clicked(b):
    global correct_answers, attempted_answers
    with output:
        student_angle = student_angle_input.value
        tolerance = 1.0  # degrees
        attempted_answers += 1

        if abs(student_angle - true_thigh_angle) <= tolerance:
            correct_answers += 1
            display(Markdown(f"✅ **Correct!** The absolute thigh angle is **{true_thigh_angle}°**."))
        else:
            display(Markdown(f"❌ **Not quite.** The correct absolute thigh angle is **{true_thigh_angle}°**. Try again!"))
    update_score_display()

# Callback to generate a new problem
def on_new_problem_clicked(b):
    global GTX, GTY, LEX, LEY, LMX, LMY, true_thigh_angle
    GTX, GTY, LEX, LEY, LMX, LMY = generate_coordinates()
    true_thigh_angle = calculate_absolute_angle(GTX, GTY, LEX, LEY)
    display_coordinates()

check_button.on_click(on_check_clicked)
new_problem_button.on_click(on_new_problem_clicked)

# Display everything
display(score_output, output)

# Show initial problem
display_coordinates()
update_score_display()
