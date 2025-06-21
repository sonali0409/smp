from django.shortcuts import render,HttpResponse
from smpapp.tasks import sample_task

# Create your views here.
# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Recipe, Rating
from .serializers import RecipeSerializer, RatingSerializer
from .permission import IsSeller, IsCustomer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSeller()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated(), IsCustomer()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


def test_view(request):
    sample_task.delay()
    return HttpResponse("Task triggered!")
