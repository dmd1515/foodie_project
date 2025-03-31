from django.shortcuts import render, redirect
from .models import TemporaryImage
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .models import TemporaryImage
# Create your views here.
def home(request):
    return render(request, 'home.html')


def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        try:
            temp_image = TemporaryImage(image=image)
            temp_image.full_clean()
            temp_image.save()
            return JsonResponse({"message": "Image uploaded successfully!", "image_id": temp_image.id})
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
    return redirect('home')


def delete_uploaded_image(request, image_id):
    if request.method == "DELETE":
        try:
            image = TemporaryImage.objects.get(id=image_id)
            image.delete()
            return JsonResponse({"message": "Image deleted successfully!"})
        except TemporaryImage.DoesNotExist:
            return JsonResponse({"error": "Image not found!"}, status=404)

    return JsonResponse({"error": "Invalid request!"}, status=400)
    
def send_message(request):
    # Tikriname, ar užklausa yra POST ir AJAX
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        message = request.POST.get('message', '').strip()  # Gauname žinutę ir pašaliname tarpus

        # Tikriname, ar žinutė yra tuščia
        if not message:
            return JsonResponse({'error': 'Message cannot be empty.'}, status=400)

        # Čia būtų logika, kuri apdoroja žinutę (pvz., išsaugojimas duomenų bazėje)
        # Pavyzdys:
        # save_message_to_database(message)

        return JsonResponse({'success': 'Message sent!'})

    # Jei užklausa netinkama, grąžiname klaidą
    return JsonResponse({'error': 'Invalid request.'}, status=400)

def home(request):
    return render(request, 'home.html')  # Grąžiname pagrindinį šabloną
