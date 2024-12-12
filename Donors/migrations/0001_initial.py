# Generated by Django 5.1.2 on 2024-11-16 10:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('address', models.TextField(default='', max_length=500)),
                ('gender', models.CharField(max_length=10)),
                ('image', models.ImageField(upload_to='')),
                ('ready_to_donate', models.BooleanField(default=True)),
                ('blood_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Donors.bloodgroup')),
                ('donor', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RequestBlood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('state', models.CharField(blank=True, max_length=200)),
                ('city', models.CharField(blank=True, max_length=300)),
                ('address', models.CharField(blank=True, max_length=500)),
                ('date', models.CharField(blank=True, max_length=100)),
                ('blood_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Donors.bloodgroup')),
            ],
        ),
    ]
