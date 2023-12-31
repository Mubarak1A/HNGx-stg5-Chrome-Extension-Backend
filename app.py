from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
import creds

app = Flask(__name__)
CORS(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure your OpenAI API key
#openai.api_key = creds.api_key

# Configure RabbitMQ connection parameters
#RABBITMQ_HOST = 'localhost'
#RABBITMQ_PORT = 5672

# Video model to store video data
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255))

# Create the database and the Video table
with app.app_context():
    db.create_all()

videos = {}

# Generate a new video ID and store an empty video record in the database
def generate_video_id():
     return str(len(videos) + 1)

# Function to update video data
def update_video_data(video_id, data):
    file_path = f'videos/{video_id}.mp4'
    with open(file_path, 'ab') as video_file:
        video_file.write(data)

# Endpoint to start a new video and get a video ID
@app.route('/start_video', methods=['POST'])
def start_video():
    video_id = generate_video_id()
    os.makedirs('videos', exist_ok=True)
    videos[video_id] = {'file_path': f'/videos/{video_id}.mp4'}
    return jsonify({'video_id': video_id})

# Endpoint to continuously update video data (simulate streaming)
@app.route('/update_video/<int:video_id>', methods=['POST'])
def update_video(video_id):
        data = request.get_data()
        update_video_data(video_id, data)
        return jsonify({'message': 'Video data updated.'})

# Endpoint to get video data
@app.route('/get_video/<int:video_id>', methods=['GET'])
def get_video(video_id):
    file_path = f'videos/{video_id}.mp4'
    
    if os.path.isfile(file_path):
         return send_from_directory('videos', f'{video_id}.mp4', mimetype='video/mp4')
    else:
        return jsonify({'error': 'Video not found.'}), 404


if __name__ == '__main__':
    app.run(debug=True)
