from .models import CommunityWork, Patient, Doctor, Appointment, HealthFacility, User, Visit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from location.models import Sector, Cell, Village
from django.urls import reverse_lazy
from django.forms import inlineformset_factory



class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(
        label=f"Password \n Password should not be similar to other personal information",
        widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"password"}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"confirm password"}),
    ) 
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role', 'profile_pic', 'chw_assigned', 'health_facility_assigned')

        widgets = {
            'username': forms.TextInput(
                attrs={"class":"form-control", "placeholder":"username"}
            ),
            
            'role': forms.Select(
                attrs={"class": "form-control select2"}
            ),
            'chw_assigned': forms.Select(
                attrs={"class": "form-control select2"}
            ),
            'health_facility_assigned': forms.Select(
                attrs={"class": "form-control select2"}
            ),
            
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['role'].required = True
        self.fields['profile_pic'].required = False
        self.fields['chw_assigned'].required = False
        self.fields['health_facility_assigned'].required = False


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ["first_name", "middle_name", "last_name", "district", "sector", "cell", "village", "phone_number", "identity","profile_pic", "email"]

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class":"form-control", "placeholder":"First Name"},
            ),
            "middle_name": forms.TextInput(
                attrs={"class":"form-control", "placeholder":"Middle Name"},
            ),
            "last_name": forms.TextInput(
                attrs={"class":"form-control", "placeholder":"Last Name"},
            ),
            "district": forms.Select(
                attrs={"class": "form-control select2", "hx-get":reverse_lazy("load-sector"), "hx-target":"#id_sector"},
            ),
            "sector": forms.Select(
                attrs={"class": "form-control select2", "hx-get":reverse_lazy("load-cell"), "hx-target":"#id_cell"},
            ),
            "cell": forms.Select(
                attrs={"class": "form-control select2", "hx-get":reverse_lazy("load-village"), "hx-target":"#id_village"},
            ),
            "village": forms.Select(
                attrs={"class": "form-control select2"},
            ),
            "phone_number": forms.TextInput(
                attrs={"class":"form-control", "placeholder":"Phone Number"},
            ),
            "identity": forms.TextInput(
                attrs={"class":"form-control", "placeholder":"ID or Passport"},
            ),
            "profile_pic": forms.FileInput(
                attrs={"class":"form-control"},
            ),
            "email": forms.EmailInput(
                attrs={"class":"form-control"},
            ),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sector'].queryset = Sector.objects.none()
        self.fields['cell'].queryset = Cell.objects.none()
        self.fields['village'].queryset = Village.objects.none()

        if 'district' in self.data:
            district_id = int(self.data.get("district"))
            self.fields['sector'].queryset = Sector.objects.filter(district=district_id)
        if 'sector' in self.data:
            sector_id = int(self.data.get("sector"))
            self.fields['cell'].queryset = Cell.objects.filter(sector=sector_id)
        if 'cell' in self.data:
            cell_id = int(self.data.get("cell"))
            self.fields['village'].queryset = Village.objects.filter(cell=cell_id)
        

class VisitForm(forms.ModelForm):

    class Meta:
        model = Visit
        fields = ['patient', 'disease','community_work', 'weight', 'bmi', 'health_facility', 'diagnize_classification']

        widgets = {
            "patient": forms.Select(
                attrs={"class":"form-control select2"},
            ),
            "disease": forms.TextInput(
                attrs={"class":"form-control", "placeholder":"Disease"},
            ),
            "weight": forms.NumberInput(
                attrs={"class":"form-control", "placeholder":"Weight"},
            ),
            "bmi": forms.NumberInput(
                attrs={"class":"form-control", "placeholder":"BMI"},
            ),
            "community_work": forms.Select(
                attrs={"class": "form-control select2"},
            ),
            "health_facility": forms.Select(
                attrs={"class": "form-control select2"},
            ),
            "diagnize_classification": forms.Select(
                attrs={"class": "form-control select2"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['health_facility'].queryset = HealthFacility.objects.filter(status='health_center')


class CommunityWorkForm(forms.ModelForm):

    class Meta:
        model = CommunityWork
        fields = ["first_name", "middle_name", "last_name", "district", "sector", "cell", "village", "phone_number", "health_facility", "email"]

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class":"form-control", "placeholder":"First Name"},
            ),
            "middle_name": forms.TextInput(
                attrs={"class":"form-control", "placeholder":"Middle Name"},
            ),
            "last_name": forms.TextInput(
                attrs={"class":"form-control", "placeholder":"Last Name"},
            ),
            "district": forms.Select(
                attrs={"class": "form-control select2", "hx-get":reverse_lazy("load-sector"), "hx-target":"#id_sector"},
            ),
            "sector": forms.Select(
                attrs={"class": "form-control select2", "hx-get":reverse_lazy("load-cell"), "hx-target":"#id_cell"},
            ),
            "cell": forms.Select(
                attrs={"class": "form-control select2", "hx-get":reverse_lazy("load-village"), "hx-target":"#id_village"},
            ),
            "village": forms.Select(
                attrs={"class": "form-control select2"},
            ),
            "phone_number": forms.TextInput(
                attrs={"class":"form-control", "placeholder":"Last Name"},
            ),
            
            "health_facility": forms.Select(
                attrs={"class": "form-control select2"},
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"},
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sector'].queryset = Sector.objects.none()
        self.fields['cell'].queryset = Cell.objects.none()
        self.fields['village'].queryset = Village.objects.none()

        if 'district' in self.data:
            district_id = int(self.data.get("district"))
            self.fields['sector'].queryset = Sector.objects.filter(district=district_id)
        if 'sector' in self.data:
            sector_id = int(self.data.get("sector"))
            self.fields['cell'].queryset = Cell.objects.filter(sector=sector_id)
        if 'cell' in self.data:
            cell_id = int(self.data.get("cell"))
            self.fields['village'].queryset = Village.objects.filter(cell=cell_id)


class DoctorForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ["first_name", "middle_name", "last_name", "district", "sector", "cell", "village", "phone_number", "health_facility", "profile_pic"]

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class":"form-control", "placeholder":"First Name"},
            ),
            "middle_name": forms.TextInput(
                attrs={"class":"form-control", "placeholder":"Middle Name"},
            ),
            "last_name": forms.TextInput(
                attrs={"class":"form-control", "placeholder":"Last Name"},
            ),
            "district": forms.Select(
                attrs={"class": "form-control select2", "hx-get":reverse_lazy("load-sector"), "hx-target":"#id_sector"},
            ),
            "sector": forms.Select(
                attrs={"class": "form-control select2", "hx-get":reverse_lazy("load-cell"), "hx-target":"#id_cell"},
            ),
            "cell": forms.Select(
                attrs={"class": "form-control select2", "hx-get":reverse_lazy("load-village"), "hx-target":"#id_village"},
            ),
            "village": forms.Select(
                attrs={"class": "form-control select2"},
            ),
            "phone_number": forms.TextInput(
                attrs={"class":"form-control", "placeholder":"Last Name"},
            ),
            
            "health_facility": forms.Select(
                attrs={"class": "form-control select2"},
            ),
            "profile_pic": forms.FileInput(
                attrs={"class": "form-control"},
            ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sector'].queryset = Sector.objects.none()
        self.fields['cell'].queryset = Cell.objects.none()
        self.fields['village'].queryset = Village.objects.none()

        if 'district' in self.data:
            district_id = int(self.data.get("district"))
            self.fields['sector'].queryset = Sector.objects.filter(district=district_id)
        if 'sector' in self.data:
            sector_id = int(self.data.get("sector"))
            self.fields['cell'].queryset = Cell.objects.filter(sector=sector_id)
        if 'cell' in self.data:
            cell_id = int(self.data.get("cell"))
            self.fields['village'].queryset = Village.objects.filter(cell=cell_id)


class HealthFacilityForm(forms.ModelForm):

    class Meta:
        model = HealthFacility
        fields = ["name", "district", "sector", "cell", "village", "director", "phone_number", "status", 'email']

        widgets = {
            "name": forms.TextInput(
                attrs={"class":"form-control", "placeholder":"First Name"},
            ),
            "district": forms.Select(
                attrs={"class": "form-control select2", "hx-get":reverse_lazy("load-sector"), "hx-target":"#id_sector"},
            ),
            "sector": forms.Select(
                attrs={"class": "form-control select2", "hx-get":reverse_lazy("load-cell"), "hx-target":"#id_cell"},
            ),
            "cell": forms.Select(
                attrs={"class": "form-control select2", "hx-get":reverse_lazy("load-village"), "hx-target":"#id_village"},
            ),
            "village": forms.Select(
                attrs={"class": "form-control select2"},
            ),
            "director": forms.Select(
                attrs={"class": "form-control select2"},
            ),
            "phone_number": forms.TextInput(
                attrs={"class":"form-control", "placeholder":"Last Name"},
            ),
            
            "status": forms.Select(
                attrs={"class": "form-control select2"},
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"},
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sector'].queryset = Sector.objects.none()
        self.fields['cell'].queryset = Cell.objects.none()
        self.fields['village'].queryset = Village.objects.none()

        if 'district' in self.data:
            district_id = int(self.data.get("district"))
            self.fields['sector'].queryset = Sector.objects.filter(district=district_id)
        if 'sector' in self.data:
            sector_id = int(self.data.get("sector"))
            self.fields['cell'].queryset = Cell.objects.filter(sector=sector_id)
        if 'cell' in self.data:
            cell_id = int(self.data.get("cell"))
            self.fields['village'].queryset = Village.objects.filter(cell=cell_id)


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ["appointment_date", "appointment_time", "arrived_at"]

        widgets = {
            "appointment_date": forms.DateInput(
                attrs={"class":"form-control"},
            ),
            "appointment_time": forms.TimeInput(
                attrs={"class":"form-control"},
            ),
            "arrived_at": forms.TimeInput(
                attrs={"class":"form-control"},
            )
        }



AppointmentFormSet = inlineformset_factory(
    Visit, Appointment,
    form=AppointmentForm,  # Use the custom form with widgets
    extra=1,
    can_delete=True
)