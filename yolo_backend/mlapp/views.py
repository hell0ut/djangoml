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
    if request.method == 'POST' and request.FILES.get('image'):
        request_received_date = datetime.datetime.now()
        new_file_name = f'{time.time()}{request.FILES["image"].name}'
        processed_image,width,height,img_to_predict = pillow_process_image(request.FILES['image'])
        url = upload_image_to_s3(processed_image,new_file_name)
        res = settings.MODEL(img_to_predict)
        request_processed_date = datetime.datetime.now()
        print('URL ',url)
        jpeg_image = io.BytesIO()
        Image.fromarray(res.render()[0]).save(jpeg_image,format='JPEG')
        url_pred = upload_image_to_s3(jpeg_image.getvalue(),'pred'+new_file_name)
        print('URL_PRED', url_pred)
        pred_label = ' '.join(res.crop(save=False)[0]['label'].split(' ')[:-1])
        image_prediction = ImagePrediction(image_link = url,
                                           prediction_results=url_pred,
                                           request_start_date= request_received_date,
                                           request_end_date = request_processed_date,
                                           image_width = width,
                                           image_height = height,
                                           predicted_label=pred_label)
        image_prediction.save()
        return JsonResponse({'message': 'Image processed successfully','result':pred_label})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    

def starting_page(request):
    if request.method == 'GET':
        return render(request,'mlapp/main.html')
