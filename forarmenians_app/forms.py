from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from betterforms.multiform import MultiModelForm
from forarmenians_app.models import *
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm


class UserRatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all().order_by('-value'), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = UserRating
        fields = ("star",)


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
    img = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = AdImage
        exclude = ('ad',)


class CountryForm(forms.ModelForm):
    class Meta:
        model = AdCountry
        fields = ('country', )


class StateForm(forms.ModelForm):
    class Meta:
        model = AdState
        fields = ('state', )


class AddressForm(forms.ModelForm):
    class Meta:
        model = AdAddress
        fields = ('address', )


class AddressLocation(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('city', 'location',)


class AddressMultiplyForm(MultiModelForm):

    form_classes = {
        'country': CountryForm,
        'state': StateForm,
        'address': AddressForm
    }


# ABC


class ABCAdForm(forms.ModelForm):

    class Meta:
        model = ABCAd
        exclude = ('address', 'created_by', 'is_active')


class ABCServiceForm(forms.Form):
    service = forms.CharField(max_length=100, required=False)
    price = forms.IntegerField(required=False)


class ABCMultiplyForm(MultiModelForm):
    form_classes = {
        'photo': PhotoForm,
        'ad': ABCAdForm,
        'address': AddressMultiplyForm,
        'service': ABCServiceForm,
    }


# Cafe

class CafeTypeForm(forms.ModelForm):
    class Meta:
        model = CafeType
        fields = '__all__'


class CafeSpecificForm(forms.ModelForm):
    class Meta:
        model = CafeSpecificType
        exclude = ('cafe',)



class CafeKitchenForm(forms.ModelForm):
    class Meta:
        model = CafeKitchenType
        exclude = ('cafe',)


class CafeForm(forms.ModelForm):
    class Meta:
        model = CafeAd
        exclude = ('address', 'created_by', 'is_active')


class CafeMultiplyForm(MultiModelForm):
    form_classes = {
        'photo': PhotoForm,
        'address': AddressMultiplyForm,
        'ad': CafeForm,
        'kitchen': CafeKitchenForm,
        'specific': CafeSpecificForm
    }


# Entertainments

class EntertainmentsForm(forms.ModelForm):
    class Meta:
        model = EntertainmentAd
        exclude = ('address', 'created_by', 'is_active')


class EntertainmentsMultiplyForm(MultiModelForm):
    form_classes = {
        'photo': PhotoForm,
        'ad': EntertainmentsForm,
        'address': AddressMultiplyForm,
    }


# Event


class EventAdForm(forms.ModelForm):
    class Meta:
        model = EventAd
        exclude = ('address', 'created_by', 'photos', 'is_active', )


class EventAdMultiply(MultiModelForm):
    form_classes = {
        'photo': PhotoForm,
        'address': AddressForm,
        'ad': EventAdForm,
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
        exclude = ('address', 'created_by', 'photos', 'is_active')


class PropertyMultiplyForm(MultiModelForm):
    form_classes = {
        'photo': PhotoForm,
        'ad': PropertyAdForm,
        'address': AddressMultiplyForm,
    }


# Job

class JobPhotoForm(forms.ModelForm):
    class Meta:
        model = AdImage
        exclude = ('ad',)
        # widgets = {
        #     'ad': forms.HiddenInput(),
        # }
        ad = forms.ModelChoiceField(
            queryset=Ad.objects.all(),
            required=False,
        )


class JobAdForm(forms.ModelForm):
    class Meta:
        model = JobAd
        fields = '__all__'


class JobKeySkillsForm(forms.ModelForm):
    class Meta:
        model = JobKeySkills
        exclude = ('job_ad',)
        required = {
            'skill': False,
        }


class JobWorkExperienceForm(forms.ModelForm):
    class Meta:
        model = JobWorkExperience
        exclude = ('job_ad',)
        required = {
            'work_place': False,
            'month': False,
            'experience': False,
        }


class JobLanguageSkillForm(forms.ModelForm):
    class Meta:
        model = JobLanguageSkill
        exclude = ('job_ad',)
        required = {
            'language': False,
            'level': False,
        }


class JobVacancyForm(forms.ModelForm):
    class Meta:
        model = JobVacancy
        exclude = ('address', 'created_by', 'photos', 'is_active',)


class JobResumeForm(forms.ModelForm):
    class Meta:
        model = JobResume
        exclude = ('address', 'created_by', 'photos', 'is_active',)


class JobVacancyMultiplyForm(MultiModelForm):
    form_classes = {
        'ad': JobVacancyForm,
        'photo': JobPhotoForm,
        'address': AddressForm,
        'languages': JobLanguageSkillForm,
        'key_skills': JobKeySkillsForm
    }


class JobResumeMultiplyForm(MultiModelForm):
    form_classes = {
        'ad': JobResumeForm,
        'photo': JobPhotoForm,
        'address': AddressForm,
        'languages': JobLanguageSkillForm,
        'experience': JobWorkExperienceForm,
        'key_skills': JobKeySkillsForm
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
        exclude = ('address', 'created_by', 'photos', 'is_active')


class VehicleMultiplyForm(MultiModelForm):
    form_classes = {
        'ad': VehicleAdForm,
    }

# Services


class ServiceAdForm(forms.ModelForm):
    class Meta:
        model = ServiceAd
        exclude = ('address', 'created_by', 'photos', 'is_active')


class ServiceAdMultiply(MultiModelForm):
    form_classes = {
        'photo': PhotoForm,
        'ad': ServiceAdForm,
        'address': AddressMultiplyForm,
    }


# Market


class MarketAdForm(forms.ModelForm):
    class Meta:
        model = MarketAd
        exclude = ('address', 'created_by', 'photos', 'is_active')


class MarketAdMultiply(MultiModelForm):
    form_classes = {
        'photo': PhotoForm,
        'ad': MarketAdForm,
        'address': AddressMultiplyForm,
    }


# Useful


class UsefulResourcesForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = UsefulResources
        exclude = ('address', 'created_by', 'photos', 'is_active')


class UsefulResourcesMultiply(MultiModelForm):
    form_classes = {
        'photo': PhotoForm,
        'ad': UsefulResourcesForm,
        'address': AddressMultiplyForm,
    }

# News


class NewsForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        exclude = ('created_by', )


class PaymentForm(PayPalPaymentsForm):
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.button_type = "buy"
        self.notify_url = "https://example.com/paypal-ipn/"
        self.return_url = "https://example.com/paypal-return/"
        self.cancel_return = "https://example.com/paypal-cancel/"
        self.image_url = "https://example.com/images/logo.png"
        self.business = settings.PAYPAL_BUSINESS_EMAIL
        self.currency_code = "USD"
        self.item_name = "Subscription"
        self.a3 = "9.99"
        self.p3 = 1
        self.t3 = "M"
        self.src = "1"


class PaymentForm(PayPalPaymentsForm):
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.button_type = "buy"
        self.notify_url = "https://example.com/paypal-ipn/"
        self.return_url = "https://example.com/paypal-return/"
        self.cancel_return = "https://example.com/paypal-cancel/"
        self.image_url = "https://example.com/images/logo.png"
        self.business = settings.PAYPAL_BUSINESS_EMAIL
        self.currency_code = "USD"
        self.item_name = "Subscription"
        self.a3 = "9.99"
        self.p3 = 1
        self.t3 = "M"
        self.src = "1"
