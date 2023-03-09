from . import views
from django.urls import path

urlpatterns = [
    path('upload-image/', views.upload_image, name='upload-image'),
    path('get-images/', views.get_images, name='get-images'),
    path('get-image/<str:pk>/', views.get_image, name='get-image'),
    path('create-link/<str:pk>/', views.create_link, name='create-link'),
]