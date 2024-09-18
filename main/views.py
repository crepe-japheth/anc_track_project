from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Role
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from .forms import PatientForm, DoctorForm, CommunityWorkForm, HealthFacilityForm, CustomUserCreationForm
from .models import Patient, HealthFacility, Visit, Transfer, CommunityWork, Appointment
from django.contrib.auth import login, logout
from location.models import District, Sector, Cell, Village


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = "main/login.html"
    fields = "__all__"
    success_message = 'Logged In successfully!'

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'main/signup.html'
    success_url = reverse_lazy('login')

class RoleRequiredMixin(LoginRequiredMixin, View):
    allowed_roles = []  # Set allowed roles in the view class

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_auth()
        if request.user.first_login and request.user.role:
            return self.handle_first_login()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return redirect('index') 
    
    def handle_no_auth(self):
        return redirect('login')
    
    def handle_first_login(self):
        return redirect('change_password')
    
class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'main/change_password.html'
    success_message = 'Password changed successfully!'
    success_url = reverse_lazy('index') 

    def form_valid(self, form):
        self.request.user.first_login = False
        self.request.user.save()
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "main/logout.html", {})

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")

class HomeView(RoleRequiredMixin, TemplateView):
    # allowed_roles = [Role.ADMIN, Role.CHW, Role.HEALTH_FACILITY, Role.HOSPITAL]
    allowed_roles = []
    template_name = 'main/index.html'

class AppointmentView(RoleRequiredMixin, TemplateView):
    # allowed_roles = [Role.ADMIN, Role.CHW, Role.HEALTH_FACILITY, Role.HOSPITAL]
    allowed_roles = []

    template_name = 'main/appointments.html'

class AddAppointmentView(TemplateView):
    allowed_roles = [Role.ADMIN, Role.CHW, Role.HEALTH_FACILITY, Role.HOSPITAL]
    template_name = 'main/add-appointment.html'

class AddPatientView(SuccessMessageMixin, CreateView):
    # allowed_roles = [Role.ADMIN, Role.HEALTH_FACILITY]
    template_name = 'main/add-patient.html'
    form_class = PatientForm
    success_url = reverse_lazy("patients")
    success_message = "patient Created successfully"

    def form_valid(self, form):
        print("Form is valid")
        print(form.data)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid", form.errors)
        print(form.data)
        return self.render_to_response(self.get_context_data(form=form))

class PatientView(ListView):
    allowed_roles = [Role.ADMIN, Role.CHW, Role.HEALTH_FACILITY, Role.HOSPITAL]
    model = Patient
    template_name = 'main/patient.html'
    paginate_by = 10
    context_object_name = 'patients'

class CurrentVisit(ListView):
    model = Visit
    template_name = 'main/current-visits.html'
    context_object_name = 'current_visits'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(status='active')
        return qs


class PatientDetail(DetailView):
    allowed_roles = [Role.ADMIN, Role.CHW, Role.HEALTH_FACILITY, Role.HOSPITAL]
    model = Patient
    template_name = 'main/patient-detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hospitals'] = HealthFacility.objects.filter(status='hospital')
        return context
    
class CurrentVisitDetail(DetailView):
    allowed_roles = [Role.ADMIN, Role.CHW, Role.HEALTH_FACILITY, Role.HOSPITAL]
    model = Visit
    template_name = 'main/current-visit-detail.html'
    context_object_name = 'visit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hospitals'] = HealthFacility.objects.filter(status='hospital')
        return context
    
def transfer_patient(request, id):
    if request.method == "POST":
        visit = get_object_or_404(Visit, id=id)
        hospital_id = int(request.POST.get("hospital"))
        hospital = HealthFacility.objects.get(id=hospital_id)
        transfer = Transfer.objects.create(
            visit=visit,
            from_health_facility=visit.health_facility,
            to_hospital=hospital,
        )
        transfer.save()
        visit.is_transferred = True
        visit.save()
        return redirect('transfers')
    else:
        return redirect('current-visits')
    

class TransferView(ListView):
    model = Transfer
    template_name = 'main/transfers.html'
    context_object_name = 'patients_transfered'
    paginate_by = 10


class DoctorsView(TemplateView):
    allowed_roles = [Role.ADMIN, Role.HEALTH_FACILITY, Role.HOSPITAL]
    template_name = 'main/doctors.html'

class DoctorDetailView(TemplateView):
    allowed_roles = [Role.ADMIN, Role.HEALTH_FACILITY, Role.HOSPITAL]
    template_name = 'main/doctor-detail.html'

class AddDoctorsView(CreateView):
    allowed_roles = [Role.ADMIN, Role.HEALTH_FACILITY, Role.HOSPITAL]
    template_name = 'main/add-doctor.html'
    form_class = DoctorForm


class AddCommunityWork(CreateView):
    template_name = 'main/add-community-work.html'
    form_class = CommunityWorkForm

class AddHealthFacilityView(CreateView):
    template_name = 'main/health-facility.html'
    form_class = HealthFacilityForm

class CommunityWork(TemplateView):
    template_name = 'main/community-work-list.html'

class HealthFacilityView(TemplateView):
    allowed_roles = [Role.ADMIN, Role.HEALTH_FACILITY, Role.HOSPITAL]
    template_name = 'main/health-facilities.html'

class HealthFacilityDetailView(TemplateView):
    allowed_roles = [Role.ADMIN, Role.HEALTH_FACILITY, Role.HOSPITAL]
    template_name = 'main/doctor-detail.html'




#HTMX View
##########
############

def load_drop_downs(request):
    id = request.GET.get("district")
    # model_str = 
    context = {
        "items": Sector.objects.filter(district=id)
    }
    return render(request, 'htmx/location_dropdown.html', context)

def load_cell_drop_downs(request):
    id = request.GET.get("sector")
    # model_str = 
    context = {
        "items": Cell.objects.filter(sector=id)
    }
    return render(request, 'htmx/location_dropdown.html', context)

def load_village_drop_downs(request):
    id = request.GET.get("cell")
    # model_str = 
    context = {
        "items": Village.objects.filter(cell=id)
    }
    return render(request, 'htmx/location_dropdown.html', context)