from django.contrib import admin
from .models import Patient, Appointment, HealthFacility, Doctor, CommunityWork, Visit, Transfer

class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 1

class VisitAdmin(admin.ModelAdmin):
    inlines = [AppointmentInline]

admin.site.register(Patient)
admin.site.register(Visit, VisitAdmin)
admin.site.register(Appointment)
admin.site.register(HealthFacility)
admin.site.register(Doctor)
admin.site.register(CommunityWork)
admin.site.register(Transfer)
