import json
import time

import requests
requests.post(
    "http://localhost:5000/api/v1/switch",
    data=json.dumps({"track_id": 5}),
    headers={"Content-Type": "application/json"}
)
time.sleep(10)
requests.post(
    "http://localhost:5000/api/v1/switch",
    data=json.dumps({"track_id": 10}),
    headers={"Content-Type": "application/json"}
)
time.sleep(10)
requests.post(
    "http://localhost:5000/api/v1/switch",
    data=json.dumps({"track_id": 15}),
    headers={"Content-Type": "application/json"}
)
time.sleep(10)

requests.post(
    "http://localhost:5000/api/v1/switch",
    data=json.dumps({"track_id": 20}),
    headers={"Content-Type": "application/json"}
)
time.sleep(10)

requests.post(
    "http://localhost:5000/api/v1/switch",
    data=json.dumps({"track_id": 25}),
    headers={"Content-Type": "application/json"}
)
time.sleep(10)

requests.post(
    "http://localhost:5000/api/v1/switch",
    data=json.dumps({"track_id": 30}),
    headers={"Content-Type": "application/json"}
)
