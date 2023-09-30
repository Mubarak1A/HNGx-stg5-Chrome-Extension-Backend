import requests
import time

video_id = 1

while True:
    data = b"This is a chunk of streaming data. "

    response = requests.post(f'http://127.0.0.1:5000/update_video/{video_id}', data=data)

    if response.status_code != 200:
        print('Error updating video:', response.json())

    time.sleep(1)
