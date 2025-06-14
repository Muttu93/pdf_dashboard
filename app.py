from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
SECTIONS = ['Material', 'Store', 'Employee']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure section folders exist
for section in SECTIONS:
    os.makedirs(os.path.join(UPLOAD_FOLDER, section), exist_ok=True)

def list_files(section):
    folder = os.path.join(app.config['UPLOAD_FOLDER'], section)
    files = []
    for filename in os.listdir(folder):
        if filename.endswith('.pdf'):
            path = os.path.join(folder, filename)
            upload_time = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')
            files.append({'name': filename, 'upload_time': upload_time})
    return files

@app.route('/', methods=['GET'])
def index():
    section = request.args.get('section', 'Store')  # Default to Store
    search_query = request.args.get('query', '').lower()
    files = list_files(section)

    if search_query:
        files = [f for f in files if search_query in f['name'].lower()]

    return render_template('index.html', sections=SECTIONS, selected=section, files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    section = request.form['section']
    file = request.files['file']
    if file and file.filename.endswith('.pdf'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], section, file.filename)
        file.save(filepath)
    return redirect(url_for('index', section=section))

@app.route('/delete', methods=['POST'])
def delete_files():
    section = request.form['section']
    selected_files = request.form.getlist('selected_files')
    for filename in selected_files:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], section, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    return redirect(url_for('index', section=section))

@app.route('/view/<section>/<filename>')
def view_file(section, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], section), filename)

import webbrowser
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)
DATA_FOLDER = 'data'
app.config['DATA_FOLDER'] = DATA_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

# your other routes here ...

if __name__ == '__main__':
    # Automatically open browser
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=False)


# if __name__ == '__main__':
#    app.run(debug=True)
