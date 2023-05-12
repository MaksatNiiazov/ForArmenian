from datetime import datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Country(models.Model):
    country = models.CharField(max_length=100)


class Ad(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.CharField(max_length=100)
    address = models.CharField(max_length=100)


class AdPhoto(models.Model):
    photo = models.ImageField(upload_to='static/img/ads_photos', null=False)
    ad_id = models.ForeignKey(Ad, on_delete=models.CASCADE)


class JobAd(models.Model):
    ad_id = models.ForeignKey(Ad, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    work_graphic = models.CharField(max_length=155)
    salary = models.IntegerField()
    experience = models.CharField(max_length=50)
    description = models.CharField(max_length=355)


class LanguageSkills(models.Model):
    job_id = models.ForeignKey(JobAd, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    level = models.CharField(max_length=50)


class VehicleBrand(models.Model):
    brand = models.CharField(max_length=50)


class VehicleCarcaseType(models.Model):
    carcase_type = models.CharField(max_length=100)


class VehicleDriveUnit(models.Model):
    drive_unit = models.CharField(max_length=100)


class VehicleAd(models.Model):
    ad_id = models.ForeignKey(Ad, on_delete=models.CASCADE)
    vehicle_title = models.CharField(max_length=255)
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE)
    mileage = models.CharField(max_length=100)
    motor_type = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    engine_volume = models.CharField(max_length=100)
    power = models.CharField(max_length=100)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)],
                                       help_text="Use the following format: <YYYY>")
    carcase_type = models.ForeignKey(VehicleCarcaseType, on_delete=models.CASCADE)
    drive_unit = models.ForeignKey(VehicleDriveUnit, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField(max_length=300)


class PropertyCategory(models.Model):
    title = models.CharField(max_length=100)


class PropertyRentalPeriod(models.Model):
    rental_period = models.CharField(max_length=15)


class PropertyPurpose(models.Model):
    property_purpose = models.CharField(max_length=30)


class PropertyAdd(models.Model):
    ad_id = models.ForeignKey(Ad, on_delete=models.CASCADE)
    category = models.ForeignKey(PropertyCategory, on_delete=models.CASCADE)
    condition = models.CharField(max_length=100)
    property_purpose = models.ForeignKey(PropertyPurpose, models.CASCADE)
    badrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    square = models.PositiveIntegerField()
    rental_period = models.ForeignKey(PropertyRentalPeriod, on_delete=models.CASCADE, blank=True)
