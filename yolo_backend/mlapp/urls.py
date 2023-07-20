from django.urls import path
from . import views

urlpatterns = [
    path('process-image/', views.process_image_view, name='process_image'),
    path('',views.starting_page)
]