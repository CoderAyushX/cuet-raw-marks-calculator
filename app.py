from flask import Flask,  render_template, request
from marks_cal import  calculate_marks

# Create an instance of the Flask class
app = Flask(__name__)

# Define a route and its corresponding function
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return 'No file uploaded'

    file = request.files['pdf_file']

    if file.filename == '':
        return 'No selected file'

    q_from = int(request.form.get('q-from'))
    q_to = int(request.form.get('q-to'))
    a_from = int(request.form.get('a-from'))
    a_to = int(request.form.get('a-to'))
    # # Use the 'number' variable for further processing

    pdf_path = 'response.pdf'
    file.save(pdf_path)

    output = calculate_marks(pdf_path,q_from=q_from,q_to=q_to,a_from=a_from,a_to=a_to)

    return render_template('output.html', marks = output)


# Run the application if the script is executed directly
# if __name__ == '__main__':
#     app.run(debug=True)