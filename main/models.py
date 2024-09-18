from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from location.models import District, Sector, Cell, Village




class Patient(models.Model):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=False)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True, blank=False)
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE, null=True, blank=False)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10,13}$', message="Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True)
    identity = models.CharField(max_length=16, unique=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pictures/')

    def get_all_visits(self):
        return self.visits.all()
    

    def __str__(self):
        return self.first_name
    

class Visit(models.Model):
    STATUS_CHOICES = [
        ('active', 'Being Taken Care of'),
        ('recovered', 'Recovered'),
        ('deceased', 'Deceased'),
    ]
    DIAGNIZE_CLASS = [
        ('green', 'Green'),
        ('red', 'Red'),
        ('orange', 'Orange'),
    ]
    patient = models.ForeignKey(Patient, related_name='visits', on_delete=models.CASCADE)
    community_work = models.ForeignKey("CommunityWork", on_delete=models.SET_NULL, null=True)
    health_facility = models.ForeignKey("HealthFacility", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    disease = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    bmi = models.DecimalField(max_digits=5, decimal_places=2)
    diagnize_classification = models.CharField(max_length=10, choices=DIAGNIZE_CLASS)
    is_transferred = models.BooleanField(default=False)  # If the patient was transferred to a hospital
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')  # Status of the visit


    def __str__(self):
        return f"Visit on {self.date} for {self.patient.first_name}"
    
class Transfer(models.Model):
    """Track patient transfers from a health center to a hospital"""
    visit = models.ForeignKey(Visit, related_name="transfers", on_delete=models.CASCADE)
    from_health_facility = models.ForeignKey("HealthFacility", on_delete=models.CASCADE, related_name="outgoing_transfers")
    to_hospital = models.ForeignKey("HealthFacility", on_delete=models.CASCADE, related_name="incoming_transfers")
    transfer_date = models.DateTimeField(auto_now_add=True)
    patient_arrived_at = models.DateTimeField(null=True, blank=True)  # When patient actually arrived at the hospital
    delay_in_hours = models.PositiveIntegerField(null=True, blank=True)  # Auto-calculated from transfer to arrival

    def __str__(self):
        return f"Transfer of {self.visit.patient} to {self.to_hospital.name}"

    # def calculate_delay(self):
    #     if self.patient_arrived_at:
    #         delay = (self.patient_arrived_at - self.transfer_date).total_seconds() / 3600
    #         self.delay_in_hours = round(delay, 2)
    #         self.save()

    def calculate_delay(self):
        if self.patient_arrived_at:
            # Ensure both datetimes are in the same format
            if timezone.is_aware(self.patient_arrived_at):
                # Make transfer_date aware if it is naive
                if timezone.is_naive(self.transfer_date):
                    self.transfer_date = timezone.make_aware(self.transfer_date)
            else:
                # Make both naive if patient_arrived_at is naive
                if timezone.is_aware(self.transfer_date):
                    self.transfer_date = timezone.make_naive(self.transfer_date)
            
            delay = (self.patient_arrived_at - self.transfer_date).total_seconds() / 3600
            self.delay_in_hours = round(delay, 2)
            self.save()
    


class Appointment(models.Model):
    patient = models.ForeignKey(Visit, on_delete=models.CASCADE, help_text='patient visit', related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    arrived_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.appointment_date} at {self.appointment_time} for {self.patient}"

HEALTH_FACILITY_STATUS = (
    ('health_center', 'health_center'),
    ('hospital', 'hospital'),
) 

class HealthFacility(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=False)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True, blank=False)
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE, null=True, blank=False)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=False)
    director = models.CharField(max_length=255, null=False, blank=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10,13}$', message="Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True)
    status = models.CharField(max_length=25, choices=HEALTH_FACILITY_STATUS, null=False, blank=False)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pictures/')


    def __str__(self) -> str:
        return self.name
    

class Doctor(models.Model):
    first_name = models.CharField(max_length=255, null=False, blank=False)
    middle_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=False)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True, blank=False)
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE, null=True, blank=False)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10,13}$', message="Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True)
    health_facility = models.ForeignKey("HealthFacility", on_delete=models.SET_NULL, null=True, blank=False)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pictures/')


    def __str__(self):
        return self.first_name
    

class CommunityWork(models.Model):
    first_name = models.CharField(max_length=255, null=False, blank=False)
    middle_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=False)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True, blank=False)
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE, null=True, blank=False)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=False)
    health_facility = models.ForeignKey(HealthFacility, on_delete=models.SET_NULL, null=True, blank=False, related_name="assigned_health_facility")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10,13}$', message="Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pictures/')



    def __str__(self):
        return self.first_name


class Role(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    CHW = "CHW", "CHW"
    HEALTH_FACILITY = "HEALTH FACILITY", "Health Facility"
    HOSPITAL = "HOSPITAL", "Hospital"
    

class User(AbstractUser):
    role = models.CharField(max_length=100, choices=Role.choices)
    profile_pic = models.ImageField('profile picture (Logo)', upload_to='images/', null=True, blank=True)
    chw_assigned = models.ForeignKey(CommunityWork ,on_delete=models.SET_NULL, blank=True, null=True)
    health_facility_assigned = models.ForeignKey(HealthFacility, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    first_login = models.BooleanField(default=True, blank=True, null=True)