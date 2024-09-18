# from django.core.management.base import BaseCommand
# from faker import Faker
# import random
# from main.models import Patient, Visit, Appointment, HealthFacility, Doctor, CommunityWork
# from location.models import District, Sector, Cell, Village

# fake = Faker()

# class Command(BaseCommand):
#     help = 'Generate fake data for testing the app'

#     def handle(self, *args, **kwargs):
#         self.generate_health_facilities()
#         self.generate_community_workers()
#         self.generate_patients()
#         self.generate_visits()
#         self.generate_appointments()
#         self.generate_doctors()
#         self.stdout.write(self.style.SUCCESS('Data generation complete!'))

#     # Generate data for HealthFacility
#     def generate_health_facilities(self, num=30):
#         districts = District.objects.all()
#         sectors = Sector.objects.all()
#         cells = Cell.objects.all()
#         villages = Village.objects.all()

#         facilities = []
#         for _ in range(num):
#             facility = HealthFacility.objects.create(
#                 name=fake.company(),
#                 district=random.choice(districts),
#                 sector=random.choice(sectors),
#                 cell=random.choice(cells),
#                 village=random.choice(villages),
#                 director=fake.name(),
#                 phone_number=fake.phone_number(),
#                 status=random.choice(['health_center', 'hospital']),
#             )
#             facilities.append(facility)
#         return facilities

#     # Generate data for CommunityWork
#     def generate_community_workers(self, num=30):
#         districts = District.objects.all()
#         sectors = Sector.objects.all()
#         cells = Cell.objects.all()
#         villages = Village.objects.all()

#         community_workers = []
#         for _ in range(num):
#             worker = CommunityWork.objects.create(
#                 first_name=fake.first_name(),
#                 middle_name=fake.first_name(),
#                 last_name=fake.last_name(),
#                 district=random.choice(districts),
#                 sector=random.choice(sectors),
#                 cell=random.choice(cells),
#                 village=random.choice(villages),
#                 phone_number=fake.phone_number(),
#                 health_facility=random.choice(HealthFacility.objects.all()),
#             )
#             community_workers.append(worker)
#         return community_workers

#     # Generate data for Patients
#     def generate_patients(self, num=30):
#         districts = District.objects.all()
#         sectors = Sector.objects.all()
#         cells = Cell.objects.all()
#         villages = Village.objects.all()

#         patients = []
#         for _ in range(num):
#             patient = Patient.objects.create(
#                 first_name=fake.first_name(),
#                 middle_name=fake.first_name(),
#                 last_name=fake.last_name(),
#                 district=random.choice(districts),
#                 sector=random.choice(sectors),
#                 cell=random.choice(cells),
#                 village=random.choice(villages),
#                 phone_number=fake.phone_number(),
#                 identity=fake.unique.ssn(),
#             )
#             patients.append(patient)
#         return patients

#     # Generate data for Visits
#     def generate_visits(self, num=30):
#         patients = Patient.objects.all()
#         community_workers = CommunityWork.objects.all()
#         health_facilities = HealthFacility.objects.all()

#         visits = []
#         for _ in range(num):
#             visit = Visit.objects.create(
#                 patient=random.choice(patients),
#                 community_work=random.choice(community_workers),
#                 health_facility=random.choice(health_facilities),
#                 transfer_to=random.choice(health_facilities),
#                 disease=fake.word(),
#                 weight=random.uniform(50.0, 100.0),
#                 bmi=random.uniform(18.0, 30.0),
#             )
#             visits.append(visit)
#         return visits

#     # Generate data for Appointments
#     def generate_appointments(self, num=30):
#         visits = Visit.objects.all()

#         appointments = []
#         for _ in range(num):
#             appointment = Appointment.objects.create(
#                 patient=random.choice(visits),
#                 appointment_date=fake.date_between(start_date='-1y', end_date='today'),
#                 appointment_time=fake.time(),
#                 arrived_at=fake.date_between(start_date='-1y', end_date='today'),
#             )
#             appointments.append(appointment)
#         return appointments

#     # Generate data for Doctors
#     def generate_doctors(self, num=30):
#         districts = District.objects.all()
#         sectors = Sector.objects.all()
#         cells = Cell.objects.all()
#         villages = Village.objects.all()

#         doctors = []
#         for _ in range(num):
#             doctor = Doctor.objects.create(
#                 first_name=fake.first_name(),
#                 middle_name=fake.first_name(),
#                 last_name=fake.last_name(),
#                 district=random.choice(districts),
#                 sector=random.choice(sectors),
#                 cell=random.choice(cells),
#                 village=random.choice(villages),
#                 phone_number=fake.phone_number(),
#                 health_facility=random.choice(HealthFacility.objects.all()),
#             )
#             doctors.append(doctor)
#         return doctors


from django.core.management.base import BaseCommand
from faker import Faker
import random
from main.models import Patient, Visit, Appointment, HealthFacility, Doctor, CommunityWork, Transfer
from location.models import District, Sector, Cell, Village

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake data for testing the app'

    def handle(self, *args, **kwargs):
        self.generate_health_facilities()
        self.generate_community_workers()
        self.generate_patients()
        self.generate_visits()
        self.generate_appointments()
        self.generate_doctors()
        # self.generate_transfers()
        self.stdout.write(self.style.SUCCESS('Data generation complete!'))

    def generate_health_facilities(self, num=30):
        districts = District.objects.all()
        sectors = Sector.objects.all()
        cells = Cell.objects.all()
        villages = Village.objects.all()

        facilities = []
        for _ in range(num):
            facility = HealthFacility.objects.create(
                name=fake.company(),
                district=random.choice([d.name for d in districts]),
                sector=random.choice([s.name for s in sectors]),
                cell=random.choice([c.name for c in cells]),
                village=random.choice([v.name for v in villages]),
                director=fake.name(),
                phone_number=fake.phone_number(),
                status=random.choice(['health_center', 'hospital']),
            )
            facilities.append(facility)
        return facilities

    def generate_community_workers(self, num=30):
        districts = District.objects.all()
        sectors = Sector.objects.all()
        cells = Cell.objects.all()
        villages = Village.objects.all()

        community_workers = []
        for _ in range(num):
            worker = CommunityWork.objects.create(
                first_name=fake.first_name(),
                middle_name=fake.first_name(),
                last_name=fake.last_name(),
                district=random.choice([d.name for d in districts]),
                sector=random.choice([s.name for s in sectors]),
                cell=random.choice([c.name for c in cells]),
                village=random.choice([v.name for v in villages]),
                phone_number=fake.phone_number(),
                health_facility=random.choice(HealthFacility.objects.all()),
            )
            community_workers.append(worker)
        return community_workers

    def generate_patients(self, num=30):
        districts = District.objects.all()
        sectors = Sector.objects.all()
        cells = Cell.objects.all()
        villages = Village.objects.all()

        patients = []
        for _ in range(num):
            patient = Patient.objects.create(
                first_name=fake.first_name(),
                middle_name=fake.first_name(),
                last_name=fake.last_name(),
                district=random.choice([d.name for d in districts]),
                sector=random.choice([s.name for s in sectors]),
                cell=random.choice([c.name for c in cells]),
                village=random.choice([v.name for v in villages]),
                phone_number=fake.phone_number(),
                identity=fake.unique.ssn(),
            )
            patients.append(patient)
        return patients

    def generate_visits(self, num=30):
        patients = Patient.objects.all()
        community_workers = CommunityWork.objects.all()
        health_facilities = HealthFacility.objects.all()

        visits = []
        for _ in range(num):
            visit = Visit.objects.create(
                patient=random.choice(patients),
                community_work=random.choice(community_workers),
                health_facility=random.choice(health_facilities),
                date=fake.date_time_between(start_date='-1y', end_date='now'),
                disease=fake.word(),
                weight=random.uniform(50.0, 100.0),
                bmi=random.uniform(18.0, 30.0),
                diagnize_classification=random.choice(['green', 'red', 'orange']),
                is_transferred=random.choice([True, False]),
                status=random.choice(['active', 'recovered', 'deceased']),
            )
            visits.append(visit)
        return visits

    def generate_appointments(self, num=30):
        visits = Visit.objects.all()

        appointments = []
        for _ in range(num):
            appointment = Appointment.objects.create(
                patient=random.choice(visits),
                appointment_date=fake.date_between(start_date='-1y', end_date='today'),
                appointment_time=fake.time(),
                arrived_at=fake.date_between(start_date='-1y', end_date='today'),
            )
            appointments.append(appointment)
        return appointments

    def generate_doctors(self, num=30):
        districts = District.objects.all()
        sectors = Sector.objects.all()
        cells = Cell.objects.all()
        villages = Village.objects.all()

        doctors = []
        for _ in range(num):
            doctor = Doctor.objects.create(
                first_name=fake.first_name(),
                middle_name=fake.first_name(),
                last_name=fake.last_name(),
                district=random.choice([d.name for d in districts]),
                sector=random.choice([s.name for s in sectors]),
                cell=random.choice([c.name for c in cells]),
                village=random.choice([v.name for v in villages]),
                phone_number=fake.phone_number(),
                health_facility=random.choice(HealthFacility.objects.all()),
            )
            doctors.append(doctor)
        return doctors

    # def generate_transfers(self, num=30):
    #     visits = Visit.objects.all()
    #     health_facilities = HealthFacility.objects.all()

    #     transfers = []
    #     for _ in range(num):
    #         transfer = Transfer.objects.create(
    #             visit=random.choice(visits),
    #             from_health_facility=random.choice(health_facilities),
    #             to_hospital=random.choice(health_facilities),
    #             transfer_date=fake.date_time_between(start_date='-1y', end_date='now'),
    #             patient_arrived_at=fake.date_time_between(start_date='-1y', end_date='now') if random.choice([True, False]) else None,
    #         )
    #         transfer.calculate_delay()
    #         transfers.append(transfer)
    #     return transfers
