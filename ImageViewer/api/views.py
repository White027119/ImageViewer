from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.response import Response 
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics 
from django.http import HttpResponse


from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .models import Image, ImageUser, ExpLink
from .serializers import ImageSerializer


@api_view(['POST'])
def login_user(request):
    username = request.data['username']
    password = request.data['password']
    user = User.objects.get(username=username)
    if user.check_password(password):
        login(request, user)
    return Response('User Logged In')

@api_view(['GET'])
def logout_user(request):
    logout(request)
    return Response('User Logged Out')

class ImageView(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = Image.objects.all()
    
    def list(self, request):
        user = self.request.user
        user_plan = ImageUser.objects.get(user=user).plan
        images = Image.objects.filter(user=user)
        r_images = []
        av_sizes = user_plan.sizes.split(',')
        

        for image in images:
            n_img = {
                'id': image.id,
                "sizes": []
            }
            for size in av_sizes:
                if size == '0':
                    n_img['sizes'].append(request.build_absolute_uri(f"{image.id}/orginal").replace('api/image-view', 'image'))
                    continue
                n_img['sizes'].append(request.build_absolute_uri(f"{image.id}/{size}").replace('api/image-view', 'image'))
            r_images.append(n_img)
        return Response(r_images)

    def create(self, request):
        image = request.FILES.get('image')
        user = request.user
        if image and user:
            Image.objects.create(image=image, user=user)
            return Response('Image Uploaded')
        return Response('Image Not Uploaded')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def image_viewer(request, id, size = ''):
    user = request.user
    user_plan = ImageUser.objects.get(user=user).plan
    import time
    if not size:
        link = ExpLink.objects.get(link=id)
        if not link:
            return Response('Link not found')
        if time.time() - link.exp_date > 0:
            return Response('Link expired')
        size = link.size
        image = Image.objects.get(id=link.image.id)
        if size == 0:
           return HttpResponse(image.image, content_type='image/png') 
        
        from PIL import Image as PImage
        from io import BytesIO

        r_im = PImage.open(image.image)
        r_im.thumbnail((image.image.width,int(size)))
        im_io = BytesIO()
        r_im.save(im_io, 'png', quality=100)
        im_io.seek(0)  
        
        return HttpResponse(im_io, content_type='image/png') 
        
    av_sizes = user_plan.sizes.split(',')

    if size == 'orginal':
        image = Image.objects.get(id=id)
        if not image or image.user.id != user.id:
            return Response('Image not found')
        return HttpResponse(image.image, content_type='image/png')

    if not size in av_sizes:
        return Response('Size not available - available sizes for your plan: ' + user_plan.sizes)
    image = Image.objects.get(id=id)
    if not image or image.user.id != user.id:
        return Response('Image not found')

    from PIL import Image as PImage
    from io import BytesIO


    r_im = PImage.open(image.image)
    r_im.thumbnail((image.image.width,int(size)))
    im_io = BytesIO()
    r_im.save(im_io, 'png', quality=100)
    im_io.seek(0)  
    
    return HttpResponse(im_io, content_type='image/png')


@api_view(['GET'])
def create_exp_link(request, id, size, time):
    image = Image.objects.get(id=id)
    user = request.user
    plan = ImageUser.objects.get(user=user).plan

    time_del = plan.exp_range.split('-')



    if not plan.create_link:
        return Response('You dont have permission to create links')
    if not image:
        return Response('Image not found')
    if not image.user.id == user.id:
        return Response('You dont have permission to create links for this image')
    if not str(size) in plan.sizes.split(','):
        return Response('Size not available - available sizes for your plan: ' + plan.sizes)
    if time<int(time_del[0]) or time>int(time_del[1]):
        return Response(f'Time out of range - available range for your plan: {time_del[0]}-{time_del[1]}')
    
    from random import randint
    from string import ascii_letters
    import time as time_
    link = ''.join([ascii_letters[randint(0, len(ascii_letters)-1)] for i in range(10)])
    exp_date = time_.time() + time
    ExpLink.objects.create(image=image, link=link, exp_date=exp_date, size=size).save()
    new_link = request.build_absolute_uri().split('api')[0] + 'image/' + link + '/'
    return Response(new_link)
    

    


