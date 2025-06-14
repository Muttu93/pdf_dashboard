import os
import webbrowser
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime

app = Flask(__name__)

# Use 'data' folder inside the project for sections
DATA_FOLDER = 'uploads'
SECTIONS = ['Material', 'Store', 'Employee']

@app.route('/')
def index():
    section = request.args.get('section', 'Material')
    files = []
    section_folder = os.path.join(DATA_FOLDER, section)
    if os.path.exists(section_folder):
        files = os.listdir(section_folder)
    files_data = []
    for file in files:
        filepath = os.path.join(section_folder, file)
        if os.path.isfile(filepath):
            upload_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            files_data.append({
                'name': file,
                'upload_time': upload_time.strftime('%Y-%m-%d %H:%M:%S'),
                'path': f'{section}/{file}'
            })
    return render_template('index.html', sections=SECTIONS, selected_section=section, files=files_data)

@app.route('/upload', methods=['POST'])
def upload():
    section = request.form.get('section', 'Material')
    file = request.files.get('file')
    if file and file.filename != '':
        save_path = os.path.join(DATA_FOLDER, section)
        os.makedirs(save_path, exist_ok=True)
        file.save(os.path.join(save_path, file.filename))
    return redirect(url_for('index', section=section))

@app.route('/delete', methods=['POST'])
def delete():
    section = request.form.get('section', 'Material')
    files_to_delete = request.form.getlist('files')
    section_folder = os.path.join(DATA_FOLDER, section)
    for file in files_to_delete:
        filepath = os.path.join(section_folder, file)
        if os.path.exists(filepath):
            os.remove(filepath)
    return redirect(url_for('index', section=section))

@app.route('/view/<path:filename>')
def view(filename):
    return send_from_directory(DATA_FOLDER, filename)

if __name__ == '__main__':
    # Auto open browser
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=False)
