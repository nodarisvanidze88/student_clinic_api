from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserCreate, AppoitmentViewset,AvailabilityViewset,DoctorViewset

router = DefaultRouter()

router.register(r'doctors', DoctorViewset)
router.register(r'appoitment', AppoitmentViewset)
router.register(r'availability', AvailabilityViewset)
urlpatterns = [
    path("register/",UserCreate.as_view(), name='register'),
    path('', include(router.urls)),
]
