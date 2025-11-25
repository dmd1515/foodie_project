from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def validate_image_size(image):
    max_size = 5 * 1024 * 1024  # 5MB in bytes
    if image.size > max_size:
        raise ValidationError("Image size exceeds 5MB")

def validate_image_format(image):
    if not image.name.lower().endswith('.jpg') and not image.name.lower().endswith('.jpeg'):
        raise ValidationError("Only JPEG images are allowed.")
    
class TemporaryImage(models.Model):
    image = models.ImageField(upload_to='temp_images/', validators=[validate_image_size, validate_image_format])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'temporaryImages'

class GeneratedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_recipes')
    content = models.TextField()
    #title = models.CharField(max_length=255)
    #ingredients = models.TextField()
    #instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'generatedRecipes'