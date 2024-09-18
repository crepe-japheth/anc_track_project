from django.db import models

class District(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.name
    
class Sector(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'
    
class Cell(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Village(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    village_code = models.CharField(max_length=150, null=True, blank=True)
    cell = models.ForeignKey(Cell, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
