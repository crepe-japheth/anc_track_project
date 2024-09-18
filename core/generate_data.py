from faker import Faker
from main.models import Patient, Visit, Appointment, HealthFacility, Doctor, CommunityWork, HEALTH_FACILITY_STATUS
from location.models import District, Sector, Cell, Village  # Import location models

fake = Faker()

# Use existing location data (no generation needed)
districts = District.objects.all()
sectors = Sector.objects.all()
cells = Cell.objects.all()
villages = Village.objects.all()

# Generate Patients (using existing locations)
for _ in range(30):
    patient = Patient(
        first_name=fake.first_name(),
        middle_name=fake.optional().name(),
        last_name=fake.last_name(),
        district=fake.random.choice(districts),  # Pick random district
        sector=fake.random.choice(sectors.filter(district=patient.district)),  # Filter sector by district
        cell=fake.random.choice(cells.filter(sector=patient.sector)),  # Filter cell by sector
        village=fake.random.choice(villages.filter(cell=patient.cell)),  # Filter village by cell
        phone_number=fake.phone_number(),
        identity=fake.ssn(),
    )
    patient.save()

# Generate Health Facilities (using existing locations)
for _ in range(10):
    facility = HealthFacility(
        name=fake.company(),
        district=fake.random.choice(districts),
        sector=fake.random.choice(sectors.filter(district=facility.district)),
        cell=fake.random.choice(cells.filter(sector=facility.sector)),
        village=fake.random.choice(villages.filter(cell=facility.cell)),
        director=fake.name(),
        phone_number=fake.phone_number(),
        status=fake.random.choice(HEALTH_FACILITY_STATUS)[0],
    )
    facility.save()

# Generate Doctors (using existing locations)
for facility in HealthFacility.objects.all():
    for _ in range(2):
        doctor = Doctor(
            first_name=fake.first_name(),
            middle_name=fake.optional().name(),
            last_name=fake.last_name(),
            district=facility.district,
            sector=facility.sector,
            cell=facility.cell,
            village=facility.village,
            phone_number=fake.phone_number(),
            health_facility=facility,
        )
        doctor.save()

# Generate Community Workers (using existing locations)
for facility in HealthFacility.objects.all():
    worker = CommunityWork(
        first_name=fake.first_name(),
        middle_name=fake.optional().name(),
        last_name=fake.last_name(),
        district=facility.district,
        sector=facility.sector,
        cell=facility.cell,
        village=facility.village,
        health_facility=facility,
        phone_number=fake.phone_number(),
    )
    worker.save()

# Generate Visits (with some random Patients)
for _ in range(30):
    patient = Patient.objects.order_by('?').first()  # Pick a random patient
    visit = Visit(
        patient=patient,
        community_work=fake.optional().instance(CommunityWork),
        health_facility=fake.optional().instance(HealthFacility),
        disease=fake.disease(),
        weight=round(fake.pydecimal(minval=40.00, maxval=100.00, positive=True), 2),
        bmi=round(fake.pydecimal(minval=18.00, maxval=25.00, positive=True), 2),
    )
    visit.save()

# Generate Appointments (with random Visits)
for visit in Visit.objects.all():
    appointment = Appointment(
        patient=visit,
        appointment_date=fake.future_date(days_between=30),
        appointment_time=fake.time(hour=list(range(9, 17)), minute=list(range(0, 60, 30))),
    )
    appointment.save()

print("Fake data generation completed!")