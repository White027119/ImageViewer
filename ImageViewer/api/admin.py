from django.contrib import admin
from .models import Image, Plan, ImageUser, ExpLink
# Register your models here.
admin.site.register(ImageUser)
admin.site.register(Image)
admin.site.register(Plan)