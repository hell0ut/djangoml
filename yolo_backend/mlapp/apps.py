from django.apps import AppConfig
import os
import torch
import requests
import json


class MlappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mlapp'
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=os.getenv('WEIGHTS_LINK'))
    s3_bucket_url = "https://qartsweightsbucketopen.s3.eu-west-3.amazonaws.com/notes.json"

    result_dict = {}

    response = requests.get(s3_bucket_url)

    if response.status_code == 200:
        data = json.loads(response.text)

        for category in data["categories"]:
            name = category["name"]
            id = category["id"]
            result_dict[name] = id

    else:
        print(f"Failed to download the JSON file. Status code: {response.status_code}")


        

