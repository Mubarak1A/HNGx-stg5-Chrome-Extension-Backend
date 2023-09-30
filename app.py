from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Video model to store video data
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary)

# Create the database and the Video table
with app.app_context():
    db.create_all()

# Generate a new video ID and store an empty video record in the database
def generate_video_id():
    video = Video(data=b'')
    db.session.add(video)
    db.session.commit()
    return video.id

# Endpoint to start a new video and get a video ID
@app.route('/start_video', methods=['POST'])
def start_video():
    video_id = generate_video_id()
    return jsonify({'video_id': video_id})

# Endpoint to continuously update video data (simulate streaming)
@app.route('/update_video/<int:video_id>', methods=['POST'])
def update_video(video_id):
    video = Video.query.get(video_id)

    if video:
        data = request.get_data()
        video.data += data
        db.session.commit()
        return jsonify({'message': 'Update received.'})
    else:
        return jsonify({'error': 'Video not found.'}), 404

# Endpoint to get video data
@app.route('/get_video/<int:video_id>', methods=['GET'])
def get_video(video_id):
    video = Video.query.get(video_id)

    if video:
        return jsonify({'video_data': video.data.decode('utf-8')})
    else:
        return jsonify({'error': 'Video not found.'}), 404


if __name__ == '__main__':
    app.run(debug=True)
