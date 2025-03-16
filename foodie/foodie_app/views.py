from django.shortcuts import render, redirect
from .models import TemporaryImage
from django.core.exceptions import ValidationError
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

def upload_image(request):
    if request.method == "POST" and request.FILES["image"]:
        image = request.FILES["image"]
        try:
            temp_image = TemporaryImage(image=image)
            temp_image.save()
            return JsonResponse({"message": "Image uploaded successfully!"})
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
    return redirect('home')