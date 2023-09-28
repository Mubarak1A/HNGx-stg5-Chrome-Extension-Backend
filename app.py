import os
from flask import Flask, request, redirect, url_for

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h1>Hello, this is the chrome extension video backend!</h1>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="video">
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['video']
    if file:
        # Save the file to the upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('hello'))


app.run(host='0.0.0.0', port=81)
