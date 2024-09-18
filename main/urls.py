from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('appointments/', views.AppointmentView.as_view(), name='appointments'),
    path('add-patient/', views.AddPatientView.as_view(), name='add-patient'),
    path('add-appointments/', views.AddAppointmentView.as_view(), name='add-appointments'),
    path('add-community-worker/', views.AddCommunityWork.as_view(), name='add-community-worker'),
    path('add-doctor/', views.AddDoctorsView.as_view(), name='add-doctor'),
    path('add-health-facility/', views.AddHealthFacilityView.as_view(), name='add-health-facility'),
    path('community-workers/', views.CommunityWork.as_view(), name='community-workers'),
    path('doctors/', views.DoctorsView.as_view(), name='doctors'),
    path('doctor-detail/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor-detail'),
    path('patient-detail/<int:pk>/', views.PatientDetail.as_view(), name='patient-detail'),
    path('patients/', views.PatientView.as_view(), name='patients'),
    path('health-facility-detail/<int:pk>/', views.HealthFacilityDetailView.as_view(), name='health-facility-detail'),
    path('health-facilities/', views.HealthFacilityView.as_view(), name='health-facilities'),
    path('transfers/', views.TransferView.as_view(), name='transfers'),
    path('transfer-patient/<int:id>/', views.transfer_patient, name='transfer-patient'),
    path('current-visits/', views.CurrentVisit.as_view(), name='current-visits'),
    path('current-visit-detail/<int:pk>/', views.CurrentVisitDetail.as_view(), name='current-visit-detail'),
    path('signup/', views.SignUpView.as_view(), name='signup'),

    path("change_password/", views.ChangePasswordView.as_view(), name="change_password"),
    # path('create_user/', create_user, name='create_user'),
    # path('update_user/<int:user_id>/', update_user, name='update_user'),

    ### HTMX URLS ####
    path("load-sector/", views.load_drop_downs, name='load-sector'),
    path("load-cell/", views.load_cell_drop_downs, name='load-cell'),
    path("load-village/", views.load_village_drop_downs, name='load-village')

]
