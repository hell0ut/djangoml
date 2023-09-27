from django.shortcuts import render
from .models import ImagePrediction
from django.http import JsonResponse
import datetime
from .apps import MlappConfig
import os
import time
from django.conf import settings
from PIL import Image
import io
import torch


def upload_image_to_s3(image_file,file_name):
    s3 = settings.S3
    bucket_name = os.getenv('BUCKET_NAME')
    
    s3.put_object(Body=image_file,Bucket=bucket_name,Key=file_name)
    location = s3.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
    url = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, file_name)
    return url


def pillow_process_image(image_file):
    img = Image.open(image_file)
    width, height = img.size
    img = img.resize((640,640))
    jpeg_image = io.BytesIO()
    img.save(jpeg_image, format='JPEG')
    return jpeg_image.getvalue(),width,height,img





def process_image_view(request):
    if request.method == 'POST':
        for file_obj_key in request.FILES.keys():
            file_obj = request.FILES[file_obj_key]
            break
        request_received_date = datetime.datetime.now()
        new_file_name = f'{time.time()}{file_obj.name}'
        processed_image,width,height,img_to_predict = pillow_process_image(file_obj)
        url = upload_image_to_s3(processed_image,new_file_name)
        #model = torch.hub.load('ultralytics/yolov5', 'custom', path=os.getenv('WEIGHTS_LINK'))
        #model.cpu()
        model = MlappConfig.model
        res = model(img_to_predict)
        request_processed_date = datetime.datetime.now()
        jpeg_image = io.BytesIO()
        Image.fromarray(res.render()[0]).save(jpeg_image,format='JPEG')
        url_pred = upload_image_to_s3(jpeg_image.getvalue(),'pred'+new_file_name)
        pred_label = '<<<<ERROR OCCURED>>>>'
        pred_id = -1
        id_db = -1
        try:
            pred_label = ' '.join(res.crop(save=False)[0]['label'].split(' ')[:-1])
            pred_id = MlappConfig.result_dict[pred_label]
            id_db = MlappConfig.df[MlappConfig.df['id_x']==int(pred_id)].iloc[0].id_y
        except:
            pass
        finally:
            image_prediction = ImagePrediction(image_link = url,
                                            prediction_results=url_pred,
                                            request_start_date= request_received_date,
                                            request_end_date = request_processed_date,
                                            image_width = width,
                                            image_height = height,
                                            predicted_label=pred_label)
            image_prediction.save()
        return JsonResponse({'message': 'Image processed successfully','predicted_label':pred_label,'predicted_id_nn':pred_id,'predicted_id_db_admin':id_db})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    

def starting_page(request):
    if request.method == 'GET':
        return render(request,'mlapp/main.html')
