import requests

BASE = "http://127.0.0.1:5000/"

# Sample data to be added
data = [
    {"name": "sleeping", "views": 80, "likes": 55},
    {"name": "playing", "views": 1500, "likes": 999},
    {"name": "dancing", "views": 1200, "likes": 300}
]

# Loop to add multiple videos
for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), json=data[i])
    if response.status_code == 201:
        print(f"Video {i} response:", response.json())
    else:
        print(f"Failed to add video {i}. Status code: {response.status_code}")

# Sending a GET request to retrieve the video with ID 2
response = requests.get(BASE + "video/2")
if response.status_code == 200:
    print(f"Video 2 data: {response.json()}")
else:
    print(f"Video 2 not found. Status code: {response.status_code}")
