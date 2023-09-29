import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from urllib.parse import quote

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

uploaded_videos = []

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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        uploaded_videos.append(file.filename)
        return redirect(url_for('index'))

@app.route('/videos')
def show_uploaded_videos():
    if uploaded_videos:
        return render_template('videos_render.html', video_filenames=uploaded_videos)
    else:
        return "No videos uploaded yet."

@app.route('/uploads', methods=['GET'])
def uploaded_video():
    filename = request.args.get('filename', '')
    filename = filename.replace(' ', '%20')
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, mimetype='video/mp4')

if __name__ == '__main__':
    # Create the upload directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
