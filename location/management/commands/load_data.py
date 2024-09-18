import pandas as pd
from django.core.management.base import BaseCommand
from location.models import District, Sector, Cell, Village
from core.settings import BASE_DIR

class Command(BaseCommand):
    help = 'Load data from Excel file into the database'

    def handle(self, *args, **kwargs):
        file_path = BASE_DIR / 'merged_output.xlsx'
        # file_path = r'C:\Users\PC\Desktop\jackproject\merged_output.xlsx'
        df = pd.read_excel(file_path, sheet_name='removedblanks')

        for index, row in df.iterrows():
            district_name = row['DISTRICT NAME']
            sector_name = row['SECTOR NAME']
            cell_name = row['CELL NAME']
            village_name = row['VILLAGE NAME']
            village_code = row['VILLAGE CODE']

            # Get or create district
            district, _ = District.objects.get_or_create(name=district_name)
            
            # Get or create sector
            sector, _ = Sector.objects.get_or_create(name=sector_name, district=district)
            
            # Get or create cell
            cell, _ = Cell.objects.get_or_create(name=cell_name, sector=sector)
            
            # Get or create village
            village, _ = Village.objects.get_or_create(name=village_name, village_code=village_code, cell=cell)

            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {village_name}'))

