from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Default values for input fields
    default_values = {
        'current_attended': 0,
        'current_conducted': 0,
        'willing_to_attend': 0,
        'conducted_to_add': 0
    }

    # Check if previous values are in session
    if 'previous_values' in session:
        default_values.update(session['previous_values'])

    if request.method == 'POST':
        # Get form data
        current_attended = int(request.form['current_attended'])
        current_conducted = int(request.form['current_conducted'])
        willing_to_attend = int(request.form['willing_to_attend'])
        conducted_to_add = int(request.form['conducted_to_add'])

        # Update default values
        default_values = {
            'current_attended': current_attended,
            'current_conducted': current_conducted,
            'willing_to_attend': willing_to_attend,
            'conducted_to_add': conducted_to_add
        }

        # Store values in session
        session['previous_values'] = default_values

        # Calculate updated values
        total_attended = current_attended + willing_to_attend
        total_conducted = current_conducted + conducted_to_add

        # Calculate attendance percentage
        if total_conducted > 0:
            attendance_percentage = round((total_attended / total_conducted) * 100, 2)
        else:
            attendance_percentage = 0

        # Calculate classes needed for 75% attendance
        if attendance_percentage < 75:
            required_classes = max(0, int((0.75 * total_conducted - total_attended) / (1 - 0.75)))
        else:
            required_classes = 0

        return render_template(
            'result.html',
            attended=total_attended,
            conducted=total_conducted,
            percentage=attendance_percentage,
            required_classes=required_classes
        )

    return render_template('index.html', previous_values=default_values)
