from django.db import models
from djongo import models as altModels
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def validate_image_size(image):
    max_size = 5 * 1024 * 1024  # 5MB in bytes
    if image.size > max_size:
        raise ValidationError("Image size exceeds 5MB")

def validate_image_format(image):
    if not image.name.lower().endswith('.jpg') and not image.name.lower().endswith('.jpeg'):
        raise ValidationError("Only JPEG images are allowed.")
    
class TemporaryImage(altModels.Model):
    imageObjectId = altModels.TextField()  # 👈 explicit PK
    image = altModels.ImageField(
        upload_to='temp_images/',
        validators=[validate_image_size, validate_image_format]
    )
    uploaded_at = altModels.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'temporaryImages'

class GeneratedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_recipes')
    tag = models.TextField()
    title = models.TextField()
    cookingTime = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'generatedRecipes'
class TopRecipe(models.Model):
    name = models.TextField()
    cookingTime = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()

    # The day for which this recipe is "top"
    top_date = models.DateField()  # <-- NEW FIELD

    # Optional: keep real creation time if you want
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'TopRecipes'