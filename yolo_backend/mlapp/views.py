from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

def process_image_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        print(image_file.name)
        print(image_file.size)
        # Process the image file here
        # ...
        return JsonResponse({'message': 'Image processed successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    

def starting_page(request):
    if request.method == 'GET':
        return render(request,'mlapp/main.html')
