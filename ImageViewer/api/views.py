from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['POST'])
def upload_image(request):
    # Check if user is authenticated
    # Check if image is either png or jpg
    # Save image to database
    return Response('Image Uploaded')

@api_view(['GET'])
def get_images(request):
    # Check if user is authenticated
    # Get all images from database
    # Return all images
    return Response('Images')

@api_view(['GET'])
def get_image(request, pk):
    # Check if user is authenticated
    # Get image from database
    # Return image
    return Response('Image')

@api_view(['GET'])
def create_link(request, pk):
    # Check if user is authenticated
    # Check if user has a plan
    # Create link
    # Return link
    return Response('Link Created')