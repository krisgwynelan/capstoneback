from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, LocationViewSet
from rest_framework.authtoken.views import obtain_auth_token
from .views import SensorDataView, FarmlandViewSet, AreaViewSet
# Create a router and register the LocationViewSet
router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'farmlands', FarmlandViewSet)
router.register(r'areas', AreaViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('api-token-auth/', obtain_auth_token), 
    path('sensor-data/', SensorDataView.as_view(), name='sensor-data'),

    path('', include(router.urls)),
]