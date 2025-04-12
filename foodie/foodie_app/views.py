from django.shortcuts import render, redirect
from .models import TemporaryImage
from PIL import Image
from django.http import JsonResponse
from .models import TemporaryImage
import torch
from io import BytesIO

# Create your views here.
def home(request):
    return render(request, 'home.html')

_model = None

def get_model():
    global _model
    if _model is None:
        _model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    return _model
def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        try:
            # Just save temporarily, no processing
            temp_image = TemporaryImage(image=request.FILES["image"])
            temp_image.save()
            
            return JsonResponse({
                "status": "success",
                "image_id": temp_image.id,
                "message": "Image saved for processing"
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

def detect_objects(request):
    if request.method == "POST":
        try:
            image_id = request.POST.get("image_id")
            temp_image = TemporaryImage.objects.get(id=image_id)
            
            # Actual YOLO processing
            img = Image.open(temp_image.image)
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            results = get_model()(img)
            detections = results.pandas().xyxy[0]
            detections = detections[detections['confidence'] > 0.4]
            
            detected_items = list(detections['name'].str.lower().unique())
            
            # Clean up
            temp_image.delete()
            
            return JsonResponse({
                "status": "success", 
                "objects": detected_items
            })
            
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
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
