from django.urls import path,include
from rest_framework_simplejwt.views import ( TokenObtainPairView,TokenRefreshView,)
from rest_framework.routers import DefaultRouter
from smpapp.views import RecipeViewSet,RatingViewSet

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]