from datetime import datetime
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Count
from django.urls import reverse
from location_field.models.plain import PlainLocationField


User = settings.AUTH_USER_MODEL


# Default Ad



class AdCountry(models.Model):
    country = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.country}'


class AdState(models.Model):
    state = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.state}'


class Location(models.Model):
    city = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['city'], zoom=7)

    def __str__(self):
        return f'{self.city}'


class AdAddress(models.Model):

    country = models.ForeignKey(AdCountry, on_delete=models.CASCADE, related_name='addresses')
    state = models.ForeignKey(AdState, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=100, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='addresses', null=True)

    def __str__(self):
        return f'{self.country} {self.state} {self.address}'


class Ad(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    address = models.ForeignKey(AdAddress, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    price = models.PositiveIntegerField(default=0, null=True, blank=True)
    currency = models.CharField(max_length=20, default='USD', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_date', '-updated_date')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        url_names = {
            'abcad': 'abc-detail',
            'cafead': 'cafe-detail',
            'entertainmentad': 'entertainments-detail',
            'eventad': 'events-detail',
            'marketad': 'market-detail',
            'vehiclead': 'vehicle-detail',
            'propertyad': 'property-detail',
            'usefulresources': 'useful-detail',
        }

        for subclass_name in url_names:
            if hasattr(self, subclass_name):
                return reverse(url_names[subclass_name], args=[getattr(self, subclass_name).pk])


class AdImage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='imgs')
    img = models.ImageField(upload_to='static/img/imgs', null=True, blank=True)


class AdComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    ad_id = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=300)
    created_date = models.DateField(auto_now=True)
    created_time = models.TimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.user} {self.ad_id}'

    class Meta:
        ordering = ('-pk',)


class AdLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    ad_id = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='likes')
    created_date = models.DateField(auto_now=True)
    created_time = models.TimeField(auto_now=True)

    @staticmethod
    def get_likes_count(ad_id):
        likes = AdLike.objects.annotate(comments_count=Count('comments_set')).filter(ad_id=ad_id)
        return likes


class RatingStar(models.Model):
    value = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        ordering = ["id"]


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    star = models.ForeignKey('RatingStar', on_delete=models.CASCADE)
    ad = models.ForeignKey('Ad', on_delete=models.CASCADE)

    def get_avg(self):
        review_avg = Rating.objects.filter(ad=self.ad).all()
        summ = 0
        for i in review_avg:
            summ += i.star.value
        count = Rating.objects.filter(ad=self.ad).count()
        if count == 0:
            count = 1
        return summ / count


class UserRating(models.Model):
    user_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ratings')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE)


# ABC


class ABCCategory(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.category}'


class ABCAd(Ad):
    category = models.ForeignKey(ABCCategory, on_delete=models.PROTECT, related_name='abc_ads')
    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True)

    def get_absolute_url(self):
        return reverse('abc-detail', args=[str(self.id)])


class ABCService(models.Model):
    abc = models.ForeignKey(ABCAd, on_delete=models.CASCADE, related_name='abs_services')
    service = models.CharField(max_length=100)
    price = models.IntegerField()


# Job

class JobWorkGraphic(models.Model):
    graphic = models.CharField(max_length=40,)

    def __str__(self):
        return f'{self.graphic}'


class JobEducation(models.Model):
    education = models.CharField(max_length=40,)

    def __str__(self):
        return f'{self.education}'


class JobFrequencyOfPayment(models.Model):
    fop = models.CharField(max_length=50, default='per month')

    def __str__(self):
        return f'{self.fop}'


class JobAd(Ad):
    work_graphic = models.ForeignKey(JobWorkGraphic, on_delete=models.PROTECT, related_name='jobs')
    education = models.ForeignKey(JobEducation, on_delete=models.PROTECT, related_name='jobs')
    frequency_of_payment = models.ForeignKey(JobFrequencyOfPayment, on_delete=models.PROTECT, related_name='jobs')
    salary_from = models.PositiveSmallIntegerField(default=1)
    salary_to = models.PositiveSmallIntegerField(default=1)


class JobKeySkills(models.Model):
    job_ad = models.ForeignKey(JobAd, on_delete=models.CASCADE, related_name='key_skills')
    skill = models.CharField(max_length=50)


class JobWorkExperience(models.Model):
    job_ad = models.ForeignKey(JobAd, on_delete=models.CASCADE, related_name='work_experiences')
    work_place = models.CharField(max_length=300)
    month = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)],
                                     help_text="How many months did you work?")
    experience = models.TextField()


class JobLanguageSkill(models.Model):
    job_ad = models.ForeignKey(JobAd, on_delete=models.CASCADE, related_name='languages')
    language = models.CharField(max_length=50)
    level = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.language}/{self.level}'


class JobVacancy(JobAd):
    responsibilities = models.TextField()
    requirements = models.TextField()

    def get_absolute_url(self):
        return reverse('job-detail-vacancy', args=[str(self.id)])


class JobResume(JobAd):
    pass

    def get_absolute_url(self):
        return reverse('job-detail-resume', args=[str(self.id)])

# Vehicle


class VehicleBrand(models.Model):
    brand = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.brand}'


class VehicleModel(models.Model):
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE, related_name='models')
    model = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.brand} {self.model}'


class VehicleCarcaseType(models.Model):
    carcase_type = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.carcase_type}'


class VehicleDriveUnit(models.Model):
    drive_unit = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.drive_unit}'


class VehicleMotorType(models.Model):
    motor_type = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.motor_type}'


class VehicleYear(models.Model):
    year = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)],
                                       help_text="Use the following format: <YYYY>")

    def __str__(self):
        return f'{self.year}'


class VehicleType(models.Model):
    type = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.type}'


class VehicleCondition(models.Model):
    condition = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.condition}'


class VehicleAd(Ad):
    type = models.ForeignKey(VehicleType, on_delete=models.PROTECT)
    model = models.ForeignKey(VehicleModel, on_delete=models.PROTECT)
    carcase_type = models.ForeignKey(VehicleCarcaseType, on_delete=models.PROTECT)
    drive_unit = models.ForeignKey(VehicleDriveUnit, on_delete=models.PROTECT)
    motor_type = models.ForeignKey(VehicleMotorType, on_delete=models.PROTECT)
    condition = models.ForeignKey(VehicleCondition, on_delete=models.PROTECT)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)],
                                       help_text="Use the following format: <YYYY>")
    engine_volume = models.IntegerField()
    mileage = models.IntegerField()
    power = models.DecimalField(decimal_places=1, max_digits=5)
    rent = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('vehicle-detail', args=[str(self.id)])


# Property


class PropertyCategory(models.Model):
    property_category = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.property_category}'


class PropertyType(models.Model):
    property_type = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.property_type}'


class PropertyRentalPeriod(models.Model):
    rental_period = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.rental_period}'


class PropertyCondition(models.Model):
    condition = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.condition}'


class PropertyBedrooms(models.Model):
    bedrooms = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.bedrooms}'


class PropertyBathrooms(models.Model):
    bathroom = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.bathroom}'


class PropertySquare(models.Model):
    square = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.square}'


class PropertyAd(Ad):
    category = models.ForeignKey(PropertyCategory, on_delete=models.PROTECT, related_name='property_ads')
    property_type = models.ForeignKey(PropertyType, models.PROTECT, related_name='property_ads')
    rental_period = models.ForeignKey(PropertyRentalPeriod, on_delete=models.PROTECT, blank=True)
    condition = models.ForeignKey(PropertyCondition, on_delete=models.PROTECT, blank=True)
    bedrooms = models.ForeignKey(PropertyBedrooms, on_delete=models.PROTECT, blank=True)
    bathrooms = models.ForeignKey(PropertyBathrooms, on_delete=models.PROTECT, blank=True)
    square = models.ForeignKey(PropertySquare, on_delete=models.PROTECT, blank=True)
    number_of_floors = models.PositiveIntegerField()
    floor = models.PositiveIntegerField()

    def get_absolute_url(self):
        return reverse('property-detail', args=[str(self.id)])


# Market


class MarketSticker(models.Model):
    sticker = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.sticker}'


class MarketCategory(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.category}'


class MarketAd(Ad):
    sticker = models.ForeignKey(MarketSticker, on_delete=models.PROTECT, related_name='ads')
    is_new = models.BooleanField(default=True)
    category = models.ForeignKey(MarketCategory, on_delete=models.CASCADE, related_name='ads')
    time_to_develop = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('market-detail', args=[str(self.id)])

# Useful resources


class UsefulResources(Ad):
    pass

    def get_absolute_url(self):
        return reverse('useful-detail', args=[str(self.id)])


# Entertainments


class EntertainmentType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.type}'


class EntertainmentAd(Ad):
    type = models.ForeignKey(EntertainmentType, on_delete=models.PROTECT, related_name='entertainment_ads')
    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True)

    def get_absolute_url(self):
        return reverse('entertainments-detail', args=[str(self.id)])


# News


class NewsCategory(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.category}'


class News(models.Model):
    category = models.ForeignKey(NewsCategory, on_delete=models.PROTECT, related_name='news')
    created_date = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='static/img/news_photos')
    news_source = models.CharField(max_length=100)
    link = models.URLField(max_length=300)
    important = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('news-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.title}'


class NewsTag(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='tags')
    tag = models.CharField(max_length=30)


# Cafe


class CafeType(models.Model):
    title = models.CharField(max_length=25, default='cafe')

    def __str__(self):
        return self.title


class CafeSpecificType(models.Model):
    specific = models.CharField(max_length=50)

    def __str__(self):
        return self.specific


class CafeKitchenType(models.Model):
    kitchen = models.CharField(max_length=30)

    def __str__(self):
        return self.kitchen


class CafeAd(Ad):
    type = models.ForeignKey(CafeType, on_delete=models.DO_NOTHING, related_name='cafe_ads')
    max_price = models.PositiveIntegerField(default=0, null=True, blank=True)
    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True)

    def get_absolute_url(self):
        return reverse('cafe-detail', args=[str(self.id)])


class CafeKitchen(models.Model):
    cafe = models.ForeignKey(CafeAd, on_delete=models.DO_NOTHING, related_name='kitchens')
    kitchen = models.ForeignKey(CafeKitchenType, on_delete=models.DO_NOTHING, related_name='cafes')


class CafeSpecific(models.Model):
    cafe = models.ForeignKey(CafeAd, on_delete=models.DO_NOTHING, related_name='specifics')
    specific = models.ForeignKey(CafeSpecificType, on_delete=models.DO_NOTHING, related_name='cafes')


# Services


class ServiceCategory(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.category}'


class ServiceAd(Ad):
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name='service_ads')
    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True)
    frequency_of_payment = models.CharField(max_length=50, default='per time')

    def get_absolute_url(self):
        return reverse('services-detail', args=[str(self.id)])


# Events


class EventCategory(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.category}'


class EventAd(Ad):
    category = models.ForeignKey(EventCategory, on_delete=models.PROTECT, related_name='event_ads')
    date = models.DateField()
    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True, null=True)
    ticket_link = models.URLField(max_length=300)

    def get_absolute_url(self):
        return reverse('events-detail', args=[str(self.id)])


