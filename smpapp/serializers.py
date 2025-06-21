from rest_framework import serializers
from .models import User, Recipe, Rating
from django.contrib.auth import get_user_model

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['seller', 'created_at']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['customer', 'created_at']