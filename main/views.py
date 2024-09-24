from django.db.models.query import QuerySet
from django.forms import BaseForm
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
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
from .forms import PatientForm, DoctorForm, CommunityWorkForm, HealthFacilityForm, CustomUserCreationForm, VisitForm, AppointmentFormSet
from .models import Patient, HealthFacility, Visit, Transfer, CommunityWork, Appointment, Doctor, User
from django.contrib.auth import login, logout
from location.models import District, Sector, Cell, Village
from django.utils import timezone
from.send_sms import send_sms
from .send_mail import anc_send_email
from .chart_data import chart_data

class RoleRequiredMixin(LoginRequiredMixin, View):
    allowed_roles = []  # Set allowed roles in the view class

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_auth()
        if request.user.first_login and request.user.role:
            return self.handle_first_login()
        # Ensure the user has a role before checking it
        # if not hasattr(request.user, 'role') or request.user.role not in self.allowed_roles:
        #     return self.handle_no_permission()
        # return super().dispatch(request, *args, **kwargs)
        if request.user.is_superuser or request.user.role in self.allowed_roles:
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('index') 
    
    def handle_no_auth(self):
        return redirect('login')
    
    def handle_first_login(self):
        return redirect('change_password')

class RoleBasedQuerysetMixin:
    """Mixin to filter objects based on the user's role"""
    
    def get_queryset(self):
        # Get the base queryset from the model defined in the view
        queryset = super().get_queryset()
        
        # Get the current user
        user = self.request.user

        # Filter by role
        if user.role == Role.CHW:
            if hasattr(user, 'chw_assigned') and user.chw_assigned:
                queryset = queryset.filter(community_work=user.chw_assigned)
            else:
                raise Http404("No CommunityWork assigned to this user.")
        
        elif user.role == Role.HEALTH_FACILITY:
            if hasattr(user, 'health_facility_assigned') and user.health_facility_assigned:
                queryset = queryset.filter(health_facility=user.health_facility_assigned)
            else:
                raise Http404("No HealthFacility assigned to this user.")
        
        elif user.role == Role.HOSPITAL:
            # If the role is hospital, we filter by hospital
            if hasattr(user, 'health_facility_assigned') and user.health_facility_assigned:
                queryset = queryset.filter(health_facility=user.health_facility_assigned)
            else:
                raise Http404("No HealthFacility assigned to this user.")
        
        # Allow admins to see all data
        elif user.role == Role.ADMIN or user.is_superuser:
            queryset = queryset.all()
        
        else:
            raise Http404("Unauthorized role.")
        
        return queryset


class UserListView(RoleRequiredMixin, RoleBasedQuerysetMixin, ListView):
    allowed_roles = [Role.ADMIN, Role.HEALTH_FACILITY, Role.HOSPITAL]
    model = User
    template_name = 'main/users.html'
    context_object_name = 'users'
    paginate_by = 10


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = "main/login.html"
    fields = "__all__"
    success_message = 'Logged In successfully!'

class SignUpView(CreateView):
    allowed_roles = [Role.ADMIN, Role.HEALTH_FACILITY, Role.HOSPITAL]
    form_class = CustomUserCreationForm
    template_name = 'main/signup.html'
    success_url = reverse_lazy('users')


    
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

class HomeView(TemplateView):
    #removed role required mixing because of too many redirects
    # allowed_roles = [Role.ADMIN, Role.CHW, Role.HEALTH_FACILITY, Role.HOSPITAL]
    allowed_roles = []
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context_data =  super().get_context_data(**kwargs)
        if user.role == Role.CHW:
            context_data['recent_transfers'] = Transfer.objects.filter(visit__community_work=user.chw_assigned)[:4]
            context_data['recent_patients'] = Visit.objects.filter(community_work=user.chw_assigned)[:4]


            context_data['total_transfer'] = Transfer.objects.filter(visit__community_work=user.chw_assigned).count()
            context_data['total_patient'] = Visit.objects.filter(community_work=user.chw_assigned).count()
            context_data['today_patient'] = Visit.objects.filter(community_work=user.chw_assigned, date=timezone.now()).count()

            context_data['visit_chart_data'] = chart_data(Visit.objects.filter(community_work=user.chw_assigned))

        elif user.role == Role.HEALTH_FACILITY:
            context_data['recent_transfers'] = Transfer.objects.filter(from_health_facility=user.health_facility_assigned)[:4]
            context_data['recent_patients'] = Visit.objects.filter(health_facility=user.health_facility_assigned)[:4]

            context_data['total_transfer'] = Transfer.objects.filter(from_health_facility=user.health_facility_assigned).count()
            context_data['total_patient'] = Visit.objects.filter(health_facility=user.health_facility_assigned).count()
            context_data['today_patient'] = Visit.objects.filter(health_facility=user.health_facility_assigned, date=timezone.now()).count()

            context_data['visit_chart_data'] = chart_data(Visit.objects.filter(health_facility=user.health_facility_assigned))

        elif user.role == Role.HOSPITAL:
            context_data['recent_transfers'] = Transfer.objects.filter(from_health_facility=user.health_facility_assigned)[:4]
            context_data['recent_patients'] = Visit.objects.filter(health_facility=user.health_facility_assigned)[:4]
            context_data['is_hospital'] = True


            context_data['total_transfer'] = Transfer.objects.filter(from_health_facility=user.health_facility_assigned).count()
            context_data['total_patient'] = Visit.objects.filter(health_facility=user.health_facility_assigned).count()
            context_data['today_patient'] = Visit.objects.filter(health_facility=user.health_facility_assigned, date=timezone.now()).count()

            context_data['visit_chart_data'] = chart_data(Visit.objects.filter(health_facility=user.health_facility_assigned))
        else:
            context_data['recent_transfers'] = Transfer.objects.all()[:4]
            context_data['recent_patients'] = Visit.objects.all()[:4]

            context_data['total_transfer'] = Transfer.objects.all().count()
            context_data['total_patient'] = Visit.objects.all().count()
            context_data['today_patient'] = Visit.objects.filter(date=timezone.now()).count()

            context_data['visit_chart_data'] = chart_data(Visit.objects.all())
            print("----------------------------")
            print(context_data['visit_chart_data'])
        return context_data

class AppointmentView(RoleRequiredMixin, ListView):
    allowed_roles = [Role.ADMIN, Role.HEALTH_FACILITY, Role.HOSPITAL]
    model = Appointment
    template_name = 'main/appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        query_set = super().get_queryset()
        if self.request.user.role == Role.CHW:
            query_set = query_set.filter(patient__community_work=self.request.user.chw_assigned)
        elif self.request.user.role == Role.HEALTH_FACILITY:
            query_set = query_set.filter(patient__health_facility=self.request.user.health_facility_assigned)
        return query_set

class AddAppointmentView(RoleRequiredMixin, TemplateView):
    allowed_roles = [Role.ADMIN, Role.CHW, Role.HEALTH_FACILITY, Role.HOSPITAL]
    template_name = 'main/add-appointment.html'

class AddPatientView(RoleRequiredMixin, SuccessMessageMixin, CreateView):
    allowed_roles = [Role.ADMIN, Role.HEALTH_FACILITY]
    template_name = 'main/add-patient.html'
    form_class = PatientForm
    success_url = reverse_lazy("patients")
    success_message = "patient Created successfully"

    def form_valid(self, form):
        # Custom logic here
        try:
            obj = Patient.objects.filter(identity=form.instance.identiy).first()
        except:
            obj = None
            print("object not found")
        if obj == None:
            form.instance.health_facility = self.request.user.health_facility_assigned
            send_sms('+250783378349', "Thanks for coming to our health center. your Information was recorded successfully")
            anc_send_email(form.instance.email, "Thanks for coming to our health center. your Information was recorded successfully")
        else:
            return redirect('patient-detail', pk=obj.pk)
        return super().form_valid(form)


class PatientView(RoleRequiredMixin, RoleBasedQuerysetMixin, ListView):
    
    allowed_roles = [Role.ADMIN, Role.HEALTH_FACILITY, Role.HOSPITAL]
    model = Patient
    template_name = 'main/patient.html'
    paginate_by = 10
    context_object_name = 'patients'

class CurrentVisit(RoleRequiredMixin, RoleBasedQuerysetMixin, ListView):
    allowed_roles = [Role.ADMIN, Role.CHW, Role.HEALTH_FACILITY, Role.HOSPITAL]
    model = Visit
    template_name = 'main/current-visits.html'
    context_object_name = 'current_visits'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(status='active')
        return qs
    

class PatientDetail(RoleRequiredMixin, DetailView):
    allowed_roles = [Role.ADMIN, Role.CHW, Role.HEALTH_FACILITY, Role.HOSPITAL]
    model = Patient
    template_name = 'main/patient-detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VisitForm()
        return context
    

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Get the current patient instance
        form = VisitForm(request.POST)
        
        if form.is_valid():
            visit = form.save(commit=False)
            visit.patient = self.object
            visit.save()
            try:
                send_sms('+250783378349', f"{visit.patient.first_name} You have been accepted by ANC Tracker ")
                anc_send_email(visit.to_hospital.email, "Thanks for coming to our health center. your Visit Information was recorded successfully")
                anc_send_email(visit.patient.email, "Thanks for coming to our health center. your Information was recorded successfully")
                anc_send_email(visit.community_work.email, "Thanks for coming to our health center. your Information was recorded successfully")
            except:
                print("failed to send email or sms")
            messages.success(request, "Visit saved successfully!")
            return HttpResponseRedirect(reverse('current-visits'))
        else:
            context = self.get_context_data()
            context['form'] = form  # Pass the invalid form back to the template
            return self.render_to_response(context)
    
class CurrentVisitDetail(RoleRequiredMixin, DetailView):
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
        try:
            send_sms('+250783378349', f"You have been transfered to {transfer.to_hospital.name}")
            anc_send_email(transfer.to_hospital.email, "Thanks for coming to our health center. your Information was recorded successfully")
            anc_send_email(transfer.visit.patient.email, "Thanks for coming to our health center. your Information was recorded successfully")
            anc_send_email(transfer.visit.community_work.email, "Thanks for coming to our health center. your Information was recorded successfully")
        except:
            print("failed to send email or sms")
        return redirect('transfers')
    else:
        return redirect('current-visits')
    

class TransferView(RoleRequiredMixin, ListView):
    allowed_roles = [Role.ADMIN, Role.CHW, Role.HEALTH_FACILITY, Role.HOSPITAL]
    model = Transfer
    template_name = 'main/transfers.html'
    context_object_name = 'patients_transfered'
    paginate_by = 10

    def get_queryset(self):
        query_set = super().get_queryset()
        if self.request.user.role == Role.CHW:
            query_set = query_set.filter(visit__community_work=self.request.user.chw_assigned)
        elif self.request.user.role == Role.HEALTH_FACILITY:
            query_set = query_set.filter(from_health_facility=self.request.user.health_facility_assigned)
        elif self.request.user.role == Role.HOSPITAL:
            query_set = query_set.filter(to_hospital=self.request.user.health_facility_assigned)

        return query_set


class DoctorsView(RoleRequiredMixin, RoleBasedQuerysetMixin, ListView):
    allowed_roles = [Role.ADMIN, Role.HEALTH_FACILITY, Role.HOSPITAL]
    model = Doctor
    template_name = 'main/doctors.html'
    context_object_name = 'doctors'
    paginate_by = 10
    

class DoctorDetailView(RoleRequiredMixin, TemplateView):
    allowed_roles = [Role.ADMIN, Role.HEALTH_FACILITY, Role.HOSPITAL]
    template_name = 'main/doctor-detail.html'

class AddDoctorsView(RoleRequiredMixin, SuccessMessageMixin, CreateView):
    allowed_roles = [Role.ADMIN, Role.HEALTH_FACILITY, Role.HOSPITAL]
    template_name = 'main/add-doctor.html'
    form_class = DoctorForm
    success_url = reverse_lazy("doctors")
    success_message = "Doctor Created successfully"


class AddCommunityWork(RoleRequiredMixin, CreateView):
    allowed_roles = [Role.ADMIN, Role.HEALTH_FACILITY]
    template_name = 'main/add-community-work.html'
    form_class = CommunityWorkForm
    success_url = reverse_lazy("community-workers")
    success_message = "Community Worker Created successfully"

class AddHealthFacilityView(RoleRequiredMixin, SuccessMessageMixin, CreateView):
    allowed_roles = [Role.ADMIN]
    template_name = 'main/health-facility.html'
    form_class = HealthFacilityForm
    success_url = reverse_lazy("health-facilities")
    success_message = "Health Facility Created successfully"

class CommunityWork(RoleRequiredMixin, RoleBasedQuerysetMixin, ListView):
    allowed_roles = [Role.ADMIN,Role.HEALTH_FACILITY]
    model = CommunityWork
    template_name = 'main/community-work-list.html'
    context_object_name = 'community_workers'
    paginate_by = 10

class HealthFacilityView(RoleRequiredMixin, ListView):
    allowed_roles = [Role.ADMIN]
    model = HealthFacility
    template_name = 'main/health-facilities.html'
    context_object_name = 'health_facilities'
    paginate_by = 10

class HealthFacilityDetailView(RoleRequiredMixin, TemplateView):
    allowed_roles = [Role.ADMIN, Role.HEALTH_FACILITY, Role.HOSPITAL]
    template_name = 'main/doctor-detail.html'



def manage_appointments(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    if request.method == 'POST':
        formset = AppointmentFormSet(request.POST, instance=visit)
        if formset.is_valid():
            formset.save()
            return redirect('current-visit-detail', visit_id=visit.id)
    else:
        formset = AppointmentFormSet(instance=visit)

    return render(request, 'main/manage_appointments.html', {'formset': formset, 'visit': visit})


def confirm_arrival(request, pk):
    transfer_obj = get_object_or_404(Transfer, id=pk)
    if transfer_obj:
        transfer_obj.patient_arrived_at = timezone.now()
        transfer_obj.save()
        messages.success(request, f'{transfer_obj.visit.patient} arrival confirmed successfully')
        return redirect('transfers')
    else:
        messages.error(request, f'{transfer_obj.visit.patient} arrival not confirmed. SOMETHING WENT WRONG')
        return redirect('transfers')

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





