# Generated by Django 5.0.7 on 2024-09-18 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_communitywork_cell_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthfacility',
            name='director',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
