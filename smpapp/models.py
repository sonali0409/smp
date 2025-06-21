from django.db import models

from django.contrib.auth.models import AbstractUser
from smpapp.tasks import compress_recipe_image

# 1. Custom User model
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.user_type})"

# 2. Recipe Model (uploaded by Sellers)
class Recipe(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'seller'})
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='recipe_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        return self.ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # save image first
        if self.image:
            print(self.image)
            compress_recipe_image.delay(self.image.name) 

    def __str__(self):
        return self.name

# 3. Rating Model (given by Customers)
class Rating(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'customer'})
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField()  # 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'recipe')  # One customer can rate a recipe only once

    def __str__(self):
        return f"{self.customer.username} rated {self.recipe.name} ({self.rating})"
    


