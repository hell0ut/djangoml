from django.contrib import admin
from .models import ImagePrediction
from django.utils.safestring import mark_safe

def display_image(obj):
    return mark_safe(f'<img src="{obj.image_link}" width="100" height="100" />')

def display_prediction(obj):
        return mark_safe(f'<img src="{obj.prediction_results}" width="100" height="100" />')

display_image.short_description = 'Image'

display_prediction.short_description = 'Image Prediction'
# Register your models here.

#admin.site.register(ImagePrediction)

@admin.register(ImagePrediction)  # Replace 'YourModel' with the name of your model
class YourModelAdmin(admin.ModelAdmin):
      readonly_fields = [display_image,display_prediction]
    
