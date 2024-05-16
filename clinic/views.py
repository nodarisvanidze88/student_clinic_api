from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import CustomUser, Availability,Appoitment,Doctor
from .serializers import CustomUserSerializer,AppoitmentSerializer,AvailabilitySerializer,DoctorSerializer
# Create your views here.
class UserCreate(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class DoctorViewset(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class AvailabilityViewset(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

class AppoitmentViewset(viewsets.ModelViewSet):
    queryset = Appoitment.objects.all()
    serializer_class = AppoitmentSerializer