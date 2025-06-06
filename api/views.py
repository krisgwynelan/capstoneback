from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication  # <- For JWT Auth
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, LocationSerializer,  FarmlandSerializer, AreaSerializer
from .models import Location, Farmland, Area
from rest_framework.views import APIView
from rest_framework import status


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# ✅ Login endpoint (returns JWT tokens)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data  # ✅ Get user from serializer
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })

# ✅ Protected Location view (based on token user)
class LocationViewSet(ModelViewSet):
    serializer_class = LocationSerializer
    authentication_classes = [JWTAuthentication]  # ✅ Use JWTAuthentication for SimpleJWT
    permission_classes = [IsAuthenticated]  # ✅ Require login

    def get_queryset(self):
        # ✅ Filter only locations belonging to the logged-in user
        return Location.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # ✅ Automatically assign the logged-in user when creating
        serializer.save(user=self.request.user)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class SensorDataView(APIView):
    def get(self, request):
        # Example static data that the ESP32 could fetch or update
        data = {
            'nitrogen': 80,
            'potassium': 75,
            'phosphorus': 55,
            'ph_level': 68,
            'moisture': 87,
            'temperature': 80
        }
        return Response(data)
    
class FarmlandViewSet(viewsets.ModelViewSet):
    queryset = Farmland.objects.all()
    serializer_class = FarmlandSerializer

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    def get_queryset(self):
        farmland_id = self.request.query_params.get('farmland_id')
        if farmland_id:
            return self.queryset.filter(farmland_id=farmland_id)
        return self.queryset.none()

    def create(self, request, *args, **kwargs):
        # To create an Area, farmland_id must be in the data
        farmland_id = request.data.get('farmland')
        if not farmland_id:
            return Response({'error': 'farmland field is required'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)