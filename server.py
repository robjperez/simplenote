from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from markdown import markdown
from bleach import linkify

import os

app = Flask(__name__)

def convert_filename_to_readable(filename):
    # Remove the .md extension
    filename = filename[:-3]

    # Split the filename into its components
    day, month, year, hour, minute, second = filename.split('_')

    # Convert to a more readable format
    readable = f"{day}-{month}-{year} {hour}:{minute}:{second}"

    return readable

@app.context_processor
def utility_processor():
    return {'convert_filename_to_readable': convert_filename_to_readable}


@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']
    filename = datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + '.md'
    with open(os.path.join('data', filename), 'w') as f:
        f.write(text)
    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete():
    filename = request.form['filename']
    os.remove(os.path.join('data', filename))
    return redirect(url_for('home'))

@app.route('/')
def home():
    files = os.listdir('data')  # list files in 'data' directory
    files.sort(key=lambda x: os.path.getmtime(os.path.join('data', x)), reverse=True)
    convertedFiles = []
    for f in files:
        with open(f'data/{f}', 'r') as f:
          content = markdown(f.read())
          content = linkify(content)
          convertedFiles.append({'name': os.path.basename(f.name), 'content': content})
    return render_template('index.html', files=convertedFiles)  # pass files to the template

if __name__ == "__main__":
    app.run(debug=True)