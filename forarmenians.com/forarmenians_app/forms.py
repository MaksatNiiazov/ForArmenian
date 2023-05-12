from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from betterforms.multiform import MultiModelForm
from forarmenians_app.models import *
from location_field.forms.plain import PlainLocationField


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all().order_by('-value'), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = Rating
        fields = ("star",)


class CommentForm(forms.ModelForm):
    class Meta:
        model = AdComment
        fields = ('comment', )


class PhotoForm(forms.ModelForm):
    class Meta:
        model = AdImage
        exclude = ('ad',)


class CountryForm(forms.ModelForm):
    class Meta:
        model = AdCountry
        fields = '__all__'


class StateForm(forms.ModelForm):
    class Meta:
        model = AdState
        fields = '__all__'


class AddressTest(forms.Form):
    city = forms.CharField()
    location = PlainLocationField(based_fields=['city'],
                                  initial='-22.2876834,-49.1607606')


class AddressForm(forms.ModelForm):

    class Meta:
        model = AdAddress
        fields = ('country', 'state', 'address', )


# ABC


class ABCAdForm(forms.ModelForm):

    class Meta:
        model = ABCAd
        exclude = ('address', 'created_by', 'photos', 'is_active')


class ABCMultiplyForm(MultiModelForm):
    form_classes = {
        'photo': PhotoForm,
        'address': AddressForm,
        'ad': ABCAdForm,
    }

# Property


class PropertyCategoryForm(forms.ModelForm):
    class Meta:
        model = PropertyCategory
        fields = '__all__'


class PropertyTypeForm(forms.ModelForm):
    class Meta:
        model = PropertyType
        fields = '__all__'


class PropertyRentalPeriodForm(forms.ModelForm):
    class Meta:
        model = PropertyRentalPeriod
        fields = '__all__'


class PropertyAdForm(forms.ModelForm):
    class Meta:
        model = PropertyAd
        exclude = ('address', 'created_by', 'photos',)


class PropertyMultiplyForm(MultiModelForm):
    form_classes = {
        'photo': PhotoForm,
        'address': AddressForm,
        'ad': PropertyAdForm,
    }


# Job


class JobAdForm(forms.ModelForm):
    class Meta:
        model = JobAd
        fields = '__all__'


class JobKeySkillsForm(forms.ModelForm):
    class Meta:
        model = JobKeySkills
        fields = '__all__'


class JobWorkExperienceForm(forms.ModelForm):
    class Meta:
        model = JobWorkExperience
        fields = '__all__'


class JobLanguageSkillForm(forms.ModelForm):
    class Meta:
        model = JobLanguageSkill
        fields = '__all__'


class JobVacancyForm(forms.ModelForm):
    class Meta:
        model = JobVacancy
        exclude = ('address', 'created_by', 'photos',)


class JobResumeForm(forms.ModelForm):
    class Meta:
        model = JobResume
        exclude = ('address', 'created_by', 'photos',)


class JobVacancyMultiplyForm(MultiModelForm):
    form_classes = {
        'job_ad': JobAdForm,
        'photo': PhotoForm,
        'address': AddressForm,
        'languages': JobLanguageSkillForm,
        'experience': JobWorkExperienceForm,
        'vacancy': JobVacancyForm,
    }



# Vehicle

class VehicleBrandFrom(forms.ModelForm):
    class Meta:
        model = VehicleBrand
        fields = '__all__'


class VehicleModelForm(forms.ModelForm):
    class Meta:
        model = VehicleModel
        fields = '__all__'


class VehicleCarcaseTypeForm(forms.ModelForm):
    class Meta:
        model = VehicleCarcaseType
        fields = '__all__'


class VehicleDriveUnitForm(forms.ModelForm):
    class Meta:
        model = VehicleDriveUnit
        fields = '__all__'


class VehicleMotorTypeForm(forms.ModelForm):
    class Meta:
        model = VehicleMotorType
        fields = '__all__'


class VehicleYearForm(forms.ModelForm):
    class Meta:
        model = VehicleYear
        fields = '__all__'


class VehicleAdForm(forms.ModelForm):
    class Meta:
        model = VehicleAd
        exclude = ('address', 'created_by', 'photos',)


class VehicleMultiplyForm(MultiModelForm):
    form_classes = {
        'photo': PhotoForm,
        'address': AddressForm,
        'ad': VehicleAdForm,
    }

# Services


class ServiceAdForm(forms.ModelForm):
    class Meta:
        model = ServiceAd
        fields = '__all__'


class ServiceAdMultiply(MultiModelForm):
    form_classes = {
        'photo': PhotoForm,
        'address': AddressForm,
        'ad': ServiceAdForm,
    }


# Market


class MarketAdForm(forms.ModelForm):
    class Meta:
        model = MarketAd
        exclude = ('address', 'created_by', 'photos',)


class MarketAdMultiply(MultiModelForm):
    form_classes = {
        'photo': PhotoForm,
        'address': AddressForm,
        'ad': MarketAdForm,
    }

# Event


class EventAdForm(forms.ModelForm):
    class Meta:
        model = EventAd
        exclude = ('address', 'created_by', 'photos',)

class EventAdMultiply(MultiModelForm):
    form_classes = {
        'photo': PhotoForm,
        'address': AddressForm,
        'ad': EventAdForm,
    }


# Useful


class UsefulResourcesForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = UsefulResources
        fields = '__all__'


# News

class NewsForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'



class Address(forms.Form):
    city = forms.CharField()
    location = PlainLocationField(based_fields=['city'],
                                  initial='-22.2876834,-49.1607606')