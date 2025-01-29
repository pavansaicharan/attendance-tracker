from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/', methods=['GET', 'POST'])
def index():
    # Default values for input fields
    default_values = {
        'current_attended': 0,
        'current_conducted': 0,
        'willing_to_attend': 0,
        'conducted_to_add': 0,
        'custom_percentage_attend': 75,
        'custom_percentage_miss': 75
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
        custom_percentage_attend = int(request.form.get('custom_percentage_attend', 75))  # Default to 75 if not provided
        custom_percentage_miss = int(request.form.get('custom_percentage_miss', 75))  # Default to 75 if not provided

        # Update default values
        default_values = {
            'current_attended': current_attended,
            'current_conducted': current_conducted,
            'willing_to_attend': willing_to_attend,
            'conducted_to_add': conducted_to_add,
            'custom_percentage_attend': custom_percentage_attend,
            'custom_percentage_miss': custom_percentage_miss
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

        # Calculate required classes for custom percentage attendance
        required_classes_custom = max(0, int((custom_percentage_attend * total_conducted - total_attended) / (1 - custom_percentage_attend / 100)))
        max_classes_miss_custom = max(0, int((total_conducted - total_attended) * (1 - custom_percentage_miss / 100)))

        # Default calculation for 75%
        required_classes_75 = max(0, int((75 * total_conducted - total_attended) / (1 - 75 / 100)))
        max_classes_miss_75 = max(0, int(total_attended - (75 / 100 * total_conducted)))

        return render_template(
            'result.html',
            attended=total_attended,
            conducted=total_conducted,
            percentage=attendance_percentage,
            required_classes_custom=required_classes_custom,
            max_classes_miss_custom=max_classes_miss_custom,
            required_classes_75=required_classes_75,
            max_classes_miss_75=max_classes_miss_75,
            custom_percentage_attend=custom_percentage_attend,
            custom_percentage_miss=custom_percentage_miss,
            required_classes=required_classes_75,
            max_classes_miss=max_classes_miss_75
        )

    return render_template('index.html', previous_values=default_values)


if __name__ == '__main__':
    app.run(debug=True)
