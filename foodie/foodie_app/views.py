from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import TemporaryImage, TopRecipe
from .models import GeneratedRecipe
from PIL import Image
from django.http import JsonResponse
from .models import TemporaryImage
import torch
from io import BytesIO
from .forms import CustomUserCreationForm     
from .recipeGeneretro import *         
import json
import ast
from django.core.serializers.json import DjangoJSONEncoder
from bson import ObjectId
from django.views.decorators.http import require_GET
from django.utils.dateparse import parse_date
from django.utils import timezone

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
def upload_image(request):

    if request.method == "POST" and request.FILES.get("image"):
        try:

            # Just save temporarily, no processing
            temp_image = TemporaryImage(image=request.FILES["image"])
            temp_image.save()
            print("Saved TemporaryImage with id:", temp_image.pk, type(temp_image.pk))

            return JsonResponse({
                "status": "success",
                "image_id": str(temp_image.pk),
                "message": "Image saved for processing"
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

def detect_objects(request):
    if request.method == "POST":
        try:
            image_id = request.POST.get("image_id")
            print("RAW image_id from POST:", image_id, type(image_id))
            if not image_id:
                return JsonResponse(
                    {"status": "error", "message": "image_id missing"},
                    status=400,
                )
           
            obj_id = ObjectId(image_id)  # string -> ObjectId
            temp_image = TemporaryImage.objects.get(pk=obj_id)

            print("Hieeee, found temp_image:", temp_image)

            # Actual YOLO processing
            img = Image.open(temp_image.image)
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            results = model(img)
            detections = results.pandas().xyxy[0]
            detections = detections[detections['confidence'] > 0.4]
            
            detected_items = list(detections['name'].str.lower().unique())
            
            # Clean up
            temp_image.delete()
            
            return JsonResponse({
                "status": "success", 
                "objects": detected_items
            })
        except TemporaryImage.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "TemporaryImage not found"},
                status=404
            )
        except Exception as e:
            import traceback
            print("detect_objects ERROR:", repr(e))
            traceback.print_exc()
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

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()          # creates the user
            return redirect('login')  # or log them in automatically if you want
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def delete_account(request):
    user = request.user
    user.delete()
    return render(request, 'accounts/login.html')

def login(request):
    return render(request, 'accounts/login.html')

@login_required
def home(request):
    return render(request, 'accounts/home.html')

def styles(request):
    return render(request, 'styles/styles.css')

@login_required
@require_POST
def save_generated_recipe(request):
    data = json.loads(request.body)
    if not data:
        return JsonResponse({'error': 'No text provided'}, status=400)

    
    obj = GeneratedRecipe.objects.create(
        user=request.user,
        title=data.get('name', 'Untitled Recipe'),
        cookingTime=data.get('cookingTime', ''),
        ingredients=data.get('ingredients', []),
        instructions=data.get('instructions', [])
    )

    return JsonResponse({'success': True, 'id': obj.id})
@require_POST
def save_top_recipe(request):
    data = json.loads(request.body or "{}")
    if not data:
        return JsonResponse({'error': 'No text provided'}, status=400)

    date_str = data.get("date")
    top_date = parse_date(date_str) if date_str else None
    if not top_date:
        return JsonResponse({'error': 'Invalid or missing date'}, status=400)

    obj = TopRecipe.objects.create(
        name=data.get('name', 'Untitled Recipe'),
        cookingTime=data.get('cookingTime', ''),
        # you’re using TextField, so store lists as JSON string
        ingredients=json.dumps(data.get('ingredients', [])),
        instructions=json.dumps(data.get('instructions', [])),
        top_date=top_date,
    )

    return JsonResponse({'success': True, 'id': str(obj.id)})

@require_GET
def get_top_recipes_by_date(request):
    """
    Returns up to 3 recipes for a given date (YYYY-MM-DD).
    Shared for all users.
    """
    date_str = request.GET.get("date")
    if not date_str:
        return JsonResponse({"recipes": []})

    date_obj = parse_date(date_str)
    if not date_obj:
        return JsonResponse({"recipes": []})

    qs = (TopRecipe.objects
          .filter(top_date=date_obj)   # <--- filter by top_date
          .order_by("id")[:3])

    recipes = []
    for r in qs:
        try:
            ingredients = json.loads(r.ingredients)
        except Exception:
            ingredients = [r.ingredients]

        try:
            instructions = json.loads(r.instructions)
        except Exception:
            instructions = [r.instructions]

        recipes.append({
            "name": r.name,
            "cookingTime": r.cookingTime,
            "ingredients": ingredients,
            "instructions": instructions,
        })

    return JsonResponse({"recipes": recipes})

@login_required
def my_recipes(request):
    qs = GeneratedRecipe.objects.filter(user=request.user).order_by('-created_at')

    recipes_data = []
    for r in qs:
        ingredients = []
        if r.ingredients:
            try:
                # if it's valid JSON: ["...","..."]
                ingredients = json.loads(r.ingredients)
            except json.JSONDecodeError:
                # if it's Python repr: ['...','...']
                ingredients = ast.literal_eval(r.ingredients)

        # Parse instructions similarly if needed
        instructions = []
        if r.instructions:
            try:
                instructions = json.loads(r.instructions)
            except json.JSONDecodeError:
                instructions = ast.literal_eval(r.instructions)

        recipes_data.append({
            "id": r.id,
            "tag": r.tag,
            "name": r.title,
            "cookingTime": r.cookingTime,
            "ingredients": ingredients,     
            "instructions": instructions,    
            "created_at": r.created_at,
        })

    return render(
            request,
            'accounts/my_recipes.html',
            {
                'recipes': qs,  
                'recipes_json': json.dumps(recipes_data, cls=DjangoJSONEncoder),
            },
        )
def top_recipes(request):
    return render(request, "top_recipes.html")

@login_required
def send_prompt(request):
    if request.method == "POST":
        data = json.loads(request.body)
        responseData = sendPrompt(data)
        return JsonResponse({'success': True, 'data':responseData})
    return JsonResponse({'error': 'Invalid request.'}, status=400)

@login_required
def edit_recipe(request, recipe_id):
    try:
        recipe = GeneratedRecipe.objects.get(id=recipe_id, user=request.user)
    except GeneratedRecipe.DoesNotExist:
        return JsonResponse({'error': 'Recipe not found.'}, status=404)

    print("hIEEEE")

    if request.method == "POST":
        data = json.loads(request.body)
        recipe.tag = data.get('tag', recipe.tag)
        recipe.title = data.get('name', recipe.title)
        recipe.cookingTime = data.get('cookingTime', recipe.cookingTime)
        recipe.ingredients = data.get('ingredients', recipe.ingredients)
        recipe.instructions = data.get('instructions', recipe.instructions)
        recipe.save()
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request.'}, status=400)