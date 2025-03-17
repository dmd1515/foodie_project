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