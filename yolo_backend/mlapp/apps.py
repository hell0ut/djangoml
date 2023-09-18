from django.apps import AppConfig
import os
import torch

class MlappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mlapp'
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=os.getenv('WEIGHTS_LINK'))


        

