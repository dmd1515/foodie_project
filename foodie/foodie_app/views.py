from django.shortcuts import render, redirect
from .models import TemporaryImage
from django.core.exceptions import ValidationError
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')


def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        try:
            temp_image = TemporaryImage(image=image)
            temp_image.full_clean()  # Užtikrina, kad bus atlikta validacija
            temp_image.save()  # Įrašo į duomenų bazę
            return JsonResponse({"message": "Image uploaded successfully!"})
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
    return redirect('home')

def send_message(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        message = request.POST.get('message', '').strip()

        if not message:
            return JsonResponse({'error': 'Message cannot be empty.'}, status=400)
            
        if len(message) > 300:
            return JsonResponse({'error': 'Message cannot exceed 300 characters.'}, status=400)

        return JsonResponse({'success': 'Message sent!'})

    return JsonResponse({'error': 'Invalid request.'}, status=400)

def home(request):
    return render(request, 'home.html')  # Grąžiname pagrindinį šabloną
