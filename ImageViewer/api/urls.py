from . import views
from django.urls import path

urlpatterns = [
    path('login-user/', views.login_user, name='login-user'),
    path('logout-user/', views.logout_user, name='logout-user'),
    path('image-view/', views.ImageView.as_view(), name='image-view'),
    path('create_link/<int:id>/<int:size>/<int:time>', views.create_exp_link, name='create-link'),
]