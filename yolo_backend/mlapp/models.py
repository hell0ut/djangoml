from django.db import models

# Create your models here.


class ImagePrediction(models.Model):
    image_link = models.URLField()
    prediction_results = models.URLField()
    request_start_date = models.DateTimeField(auto_now_add=True)
    request_end_date = models.DateTimeField(null=True, blank=True)
    image_width = models.PositiveIntegerField()
    image_height = models.PositiveIntegerField()
    predicted_label = models.CharField(max_length=255)

    def __str__(self):
        return self.image_link
