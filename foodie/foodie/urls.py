"""
URL configuration for foodie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from foodie_app import views
from foodie_app.views import send_message  # Importuojame send_message view iš foodie_app aplikacijos
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('upload/', views.upload_image, name='upload_image'),
    path('send-message/', send_message, name='send_message'),
    path('delete_uploaded_image/<int:image_id>/', views.delete_uploaded_image, name='delete_uploaded_image'), 
    path('detect/', views.detect_objects, name='detect_objects'),
]



