from django.contrib import admin
from django.urls import path
from foodie_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload_image', views.upload_image, name='upload_image'),
    path('send_message', views.send_message, name='send_message'),
    path('admin/', admin.site.urls),
]
