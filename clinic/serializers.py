from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import CustomUser, Doctor, Appoitment,Availability
from django.utils import timezone
class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", 'username', 'email', 'status', 'password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user
    

class DoctorSerializer(ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset = CustomUser.objects.filter(status="doctor"),
        write_only = True,
        source = 'user'
    )
    class Meta:
        model = Doctor
        fields = '__all__'

class AppoitmentSerializer(ModelSerializer):
    patient = CustomUserSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset = CustomUser.objects.filter(status="patient"),
        write_only = True,
        source='patient',
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset = Doctor.objects.all(),
        write_only = True,
        source = 'doctor'
    )
    class Meta:
        model = Appoitment
        fields = '__all__'
    
    def validate(self, data):
        scheduled_time = data.get('scheduled_time')
        treatment_duration = data.get('treatment_duration')
        doctor = data.get('doctor')
        print(scheduled_time)
        print(treatment_duration)
        print(doctor)
        if not scheduled_time or not treatment_duration or not doctor:
            raise serializers.ValidationError("Scheduled data, treatment duration and doctor shuld be provided")
        
        end_time = scheduled_time + timezone.timedelta(minutes=treatment_duration)
        overlaping_appoitment = Appoitment.objects.filter(
            doctor = doctor,
            scheduled_time__lt = end_time, # 10
            scheduled_time__gte = scheduled_time, # 9:45
        )
        if overlaping_appoitment.exists():
            raise serializers.ValidationError("At that moment the doctor is busy")
        availability = Availability.objects.filter(doctor=doctor)
        for available in availability:
            if available.start_time<= scheduled_time<=available.end_time:
                return data
        raise serializers.ValidationError("The Doctor is not available")


class AvailabilitySerializer(ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset = Doctor.objects.all(),
        write_only = True,
        source = "doctor"
    )
    class Meta:
        model = Availability
        fields = '__all__'