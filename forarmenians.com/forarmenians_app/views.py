from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, OuterRef, Exists, Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from forarmenians_app.forms import *
from forarmenians_app.models import *
from user_auth.models import User


class LockedView(LoginRequiredMixin):
    login_url = "login"


class MainPageView(ListView):
    template_name = "mainPage/index.html"
    model = PropertyAd

    def get_queryset(self):
        return PropertyAd.objects.all()[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = ServiceAd.objects.all()[:8]
        context['jobs'] = JobVacancy.objects.all()[:6]
        context['abc'] = ABCAd.objects.all()[:7]
        context['cafes'] = CafeAd.objects.all()[:3]
        context['entertainments'] = EntertainmentAd.objects.all()[:3]
        context['useful_resources'] = UsefulResources.objects.all()[:3]
        context['news'] = News.objects.all()[:4]
        context['events'] = EventAd.objects.all()[:3]
        return context


class AdListView(ListView):
    model = None
    template_name = None

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(sum_of_values=(Sum('rating__star')/Count('rating__star')))
        if not self.request.user.is_anonymous:
            queryset = queryset.annotate(has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))
        return queryset


class AdDetailView(DetailView):
    model = None
    template_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = AdComment.objects.filter(ad_id=self.object.id)
        context['ads'] = Ad.objects.filter(created_by=self.object.created_by)
        a, b = self.object.address.location.location.split(',')
        context['lat'] = a
        context['lng'] = b
        if not self.request.user.is_anonymous:
            context['like'] = AdLike.objects.filter(ad_id=self.kwargs['pk'], user=self.request.user)
            context['star_form'] = RatingForm
            context['rating'] = self.get_star()
            context['avg'] = self.get_avg()

        return context

    def get_star(self):
        if Rating.objects.filter(user=self.request.user, ad=self.object):
            a = Rating.objects.filter(user=self.request.user, ad=self.object).first().star.value
            if a == 5:
                return 1
            elif a == 4:
                return 2
            elif a == 3:
                return 3
            elif a == 2:
                return 4
            elif a == 1:
                return 5
            return 0

    def get_avg(self):
        review_avg = Rating.objects.filter(ad=self.object).all()
        summ = 0
        for i in review_avg:
            summ += i.star.value
        count = Rating.objects.filter(ad=self.object).count()
        if count == 0:
            count = 1
        return summ / count


class AdCreateView(LockedView, CreateView):
    model = None
    form_class = None
    template_name = None

    def form_valid(self, form):
        user = User.objects.get(email=self.request.user)
        state = AdState.objects.get(id=form['address']['state'].value())
        country = AdCountry.objects.get(id=form['address']['country'].value())
        address_ = form['address']['address'].value()
        address = form['address'].save(commit=False)
        address.state = state
        address.country = country
        address.address = address_
        address.save()
        ad = form['ad'].save(commit=False)
        ad.created_by = user
        ad.address = address
        ad.save()
        photo = form['photo'].save(commit=False)
        photo.ad_id = ad
        photo.save()
        return redirect('main')


class AddCommentView(View):

    def post(self, request, pk):
        form = CommentForm(request.POST)
        print('take form')
        user = User.objects.get(email=self.request.user)
        print('take user')
        ad = Ad.objects.get(id=self.kwargs['pk'])
        print('take ad')

        if form.is_valid():
            print(' form is valid')

            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.ad_id = ad
            form.user = user
            form.save()

        return redirect(request.META.get('HTTP_REFERER'))


class AddLikeView(View):

    def post(self, request, pk):
        ad = Ad.objects.get(id=pk)
        user = User.objects.get(email=self.request.user)

        if AdLike.objects.filter(ad_id=ad.id, user=user.id):
            unlike = AdLike.objects.get(ad_id=ad.id, user=user.id)
            unlike.delete()
        else:
            like = AdLike()
            like.user = user
            like.ad_id = ad
            like.save()
        return redirect(request.META.get('HTTP_REFERER'))


class AddStarRating(View):

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                user=self.request.user,
                ad_id=int(request.POST.get("ad")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(ststus=201)
        else:
            return HttpResponse(ststus=400)


# ABC


class ABCView(AdListView):
    model = ABCAd
    template_name = "abc/abc.html"


class ABCDetailView(AdDetailView):
    model = ABCAd
    template_name = "abc/abc-single.html"


class ABCAdCreate(AdCreateView):
    model = ABCAd
    form_class = ABCMultiplyForm
    template_name = 'abc/create_test.html'
    # fields = (
    #     'city',
    #     'location',
    # )



class ABCAdUpdateView(LockedView, UpdateView):
    model = MarketAd
    form_class = MarketAdForm
    success_url = reverse_lazy('main')
    template_name = 'abc/update_test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_id'] = self.kwargs['pk']
        return context

    def get_form_kwargs(self):
        kwargs = super(ABCAdUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'ad': self.object,
            'address': self.object.address,
        })
        return kwargs

    def form_valid(self, form):
        ad = form['ad'].save(commit=False)
        ad.save()
        photo = form['photo'].save(commit=False)
        photo.ad_id = ad
        photo.save()
        return redirect('main')

    def get_queryset(self):
        queryset = super(ABCAdUpdateView, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset


# Café


class CafeView(AdListView):
    model = CafeAd
    template_name = "cafe/cafe.html"


class CafeDetailView(AdDetailView):
    model = CafeAd
    template_name = "cafe/cafe-single.html"


# Entertainments


class EntertainmentsView(ListView):
    model = EntertainmentAd
    template_name = "entertainments/entertainments.html"


class EntertainmentsDetailView(AdDetailView):
    model = EntertainmentAd
    template_name = "entertainments/entertainments-single.html"


# Events


class EventsView(ListView):
    model = EventAd
    template_name = "events/events.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['first_place'] = AdPhoto.objects.all().order_by('-id')[:1]
        context['second_place'] = AdPhoto.objects.all().order_by('-id')[1:3]
        context['third_place'] = AdPhoto.objects.all().order_by('-id')[3:6]

        return context


class EventsDetailView(DetailView):
    model = EventAd
    template_name = "events/events-single.html"


class EventCreateView(AdCreateView):
    model = EventAd
    form_class = EventAdMultiply
    template_name = 'events/create_test.html'


class EventAdUpdateView(LockedView, UpdateView):
    model = EventAd
    form_class = EventAdMultiply
    success_url = reverse_lazy('main')
    template_name = 'abc/update_test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_id'] = self.kwargs['pk']
        return context

    def get_form_kwargs(self):
        kwargs = super(EventAdUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'ad': self.object,
            'address': self.object.address,
        })
        return kwargs

    def form_valid(self, form):
        ad = form['ad'].save(commit=False)
        ad.save()
        photo = form['photo'].save(commit=False)
        photo.ad_id = ad
        photo.save()
        return redirect('main')

    def get_queryset(self):
        queryset = super(EventAdUpdateView, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset


# Job


class JobView(TemplateView):
    template_name = "job/job.html"


class JobCatalogResumeView(AdListView):
    model = JobResume
    template_name = "job/job-catalog-resume.html"


class JobResumeDetailView(DetailView):
    model = JobResume
    template_name = "job/job-single-resume.html"


class JobCatalogVacancyView(AdListView):
    model = JobVacancy
    template_name = "job/job-catalog-vacancy.html"


class JobVacancyDetailView(DetailView):
    model = JobVacancy
    template_name = "job/job-single-vacancy.html"


class JobVacancyCreateView(CreateView):
    model = JobVacancy
    form_class = JobVacancyMultiplyForm
    template_name = 'job/create-test.html'


# Market


class MarketAdView(AdListView):
    model = MarketAd
    template_name = "market/market.html"


class MarketCreateView(AdCreateView):
    model = MarketAd
    form_class = MarketAdMultiply
    template_name = 'market/create_test.html'


class MarketAdUpdateView(LockedView, UpdateView):
    model = MarketAd
    form_class = MarketAdMultiply
    success_url = reverse_lazy('main')
    template_name = 'market/update_test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_id'] = self.kwargs['pk']
        return context

    def get_form_kwargs(self):
        kwargs = super(MarketAdUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'ad': self.object,
            'address': self.object.address,
        })
        return kwargs

    def form_valid(self, form):
        ad = form['ad'].save(commit=False)
        ad.save()
        photo = form['photo'].save(commit=False)
        photo.ad_id = ad
        photo.save()
        return redirect('main')

    def get_queryset(self):
        queryset = super(MarketAdUpdateView, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset


# News


class NewsView(ListView):
    model = News
    template_name = "news/news.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_anonymous:
            queryset = queryset.annotate(has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))
        return queryset


class NewsDetailView(DetailView):
    model = News
    template_name = "news/news-single.html"


# Profile


class ProfileView(TemplateView):
    template_name = "profile/profile.html"


class ProfileADCView(TemplateView):
    template_name = "profile/profile-ads.html"


class ProfileWalletView(TemplateView):
    template_name = "profile/profile-wallet.html"


# Property


class PropertyView(TemplateView):
    template_name = "property/property.html"


class PropertyCatalogRentView(ListView):
    model = PropertyAd
    template_name = "property/property-catalog.html"

    def get_queryset(self):
        queryset = PropertyAd.objects.filter(category=1)
        queryset = queryset.annotate(sum_of_values=(Sum('rating__star')/Count('rating__star')))
        queryset = queryset.annotate(has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat'] = False
        context['categories'] = PropertyCategory.objects.all()
        context['condition'] = PropertyCondition.objects.all()
        context['rental_period'] = PropertyRentalPeriod.objects.all()
        context['square'] = PropertySquare.objects.all()
        context['bedrooms'] = PropertyBedrooms.objects.all()
        context['bathrooms'] = PropertyBathrooms.objects.all()

        return context


class PropertyCatalogBuyView(ListView):
    model = PropertyAd
    template_name = "property/property-catalog.html"

    def get_queryset(self):
        queryset = PropertyAd.objects.filter(category=2)
        queryset = queryset.annotate(sum_of_values=(Sum('rating__star')/Count('rating__star')))
        queryset = queryset.annotate(has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat'] = True
        context['categories'] = PropertyCategory.objects.all()
        context['condition'] = PropertyCondition.objects.all()
        context['rental_period'] = PropertyRentalPeriod.objects.all()
        context['square'] = PropertySquare.objects.all()
        context['bedrooms'] = PropertyBedrooms.objects.all()
        context['bathrooms'] = PropertyBathrooms.objects.all()


        return context


class PropertyFilterBuyView(ListView):
    model = PropertyAd
    template_name = "property/property-catalog.html"

    def get_queryset(self):
        queryset = PropertyAd.objects.filter(
                        Q(property_type_id__in=self.request.GET.getlist('type-property')) |
                        Q(price__gt=self.request.GET.get('price-min'), price__lte=self.request.GET.get('price-max')) |
                        Q(condition_id__in=self.request.GET.getlist('condition')) |
                        Q(category_id__in=self.request.GET.getlist('category')) |
                        Q(bathrooms_id__in=self.request.GET.get('floor-min')) |
                        Q(floor__gt=self.request.GET.get('floor-min'), floor__lte=self.request.GET.get('floor-max')) |
                        Q(number_of_floors__gt=self.request.GET.get('quantity-floor-min'), number_of_floors__lte=self.request.GET.get('quantity-floor-max')) |
                        Q(square_id__in=self.request.GET.getlist('square')) |
                        Q(rental_period=self.request.GET.get('time'))).distinct()

        queryset = queryset.annotate(sum_of_values=(Sum('rating__star')/Count('rating__star')))
        queryset = queryset.annotate(has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = PropertyCategory.objects.all()
        context['condition'] = PropertyCondition.objects.all()
        context['rental_period'] = PropertyRentalPeriod.objects.all()
        context['square'] = PropertySquare.objects.all()
        context['bedrooms'] = PropertyBedrooms.objects.all()
        context['bathrooms'] = PropertyBathrooms.objects.all()

        return context


class PropertyDetailView(DetailView):
    model = PropertyAd
    template_name = "property/property-single.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.created_by == self.request.user:
            context['update'] = True
        return context


class PropertyAdCreate(AdCreateView):
    model = PropertyAd
    form_class = PropertyMultiplyForm
    template_name = 'property/property_create_test.html'
    success_url = reverse_lazy('main')


class PropertyAdUpdateView(LockedView, UpdateView):
    model = PropertyAd
    form_class = PropertyMultiplyForm
    success_url = reverse_lazy('main')
    template_name = 'property/property_update_test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_id'] = self.kwargs['pk']
        return context

    def get_form_kwargs(self):
        kwargs = super(PropertyAdUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'ad': self.object,
            'address': self.object.address,
        })
        return kwargs

    def form_valid(self, form):
        ad = form['ad'].save(commit=False)
        ad.save()
        photo = form['photo'].save(commit=False)
        photo.ad_id = ad
        photo.save()
        return redirect('main')

    def get_queryset(self):
        queryset = super(PropertyAdUpdateView, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset


# Useful


class UsefulView(ListView):
    model = UsefulResources
    template_name = "useful/useful.html"


class UsefulDetailView(AdDetailView):
    template_name = "useful/useful-single.html"
    model = UsefulResources


# Vehicle


class ChooceCategoriesView(TemplateView):
    template_name = "vehicle/choose-categories.html"


class VehicleView(TemplateView):
    template_name = "vehicle/vehicle.html"


class VehicleCatalogView(ListView):
    model = VehicleAd
    template_name = "vehicle/vehicle-catalog.html"

    def get_queryset(self):
        queryset = VehicleAd.objects.filter(rent=False)
        queryset = queryset.annotate(sum_of_values=(Sum('rating__star')/Count('rating__star')))
        queryset = queryset.annotate(has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))
        return queryset


class VehicleCatalogRentView(ListView):

    model = VehicleAd
    template_name = "vehicle/vehicle-catalog.html"

    def get_queryset(self):
        queryset = VehicleAd.objects.filter(rent=True)
        queryset = queryset.annotate(sum_of_values=(Sum('rating__star')/Count('rating__star')))
        queryset = queryset.annotate(has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))
        return queryset


class VehicleFilterView(ListView):
    model = VehicleAd
    template_name = "vehicle/vehicle-catalog.html"

    def get_queryset(self):

        queryset = VehicleAd.objects.filter(
                        Q(property_type_id__in=self.request.GET.getlist('type-property')) |
                        Q(price__gt=self.request.GET.get('price-min'), price__lte=self.request.GET.get('price-max')) |
                        Q(condition_id__in=self.request.GET.getlist('condition')) |
                        Q(category_id__in=self.request.GET.getlist('category')) |
                        Q(bathrooms_id__in=self.request.GET.get('floor-min')) |
                        Q(floor__gt=self.request.GET.get('floor-min'), floor__lte=self.request.GET.get('floor-max')) |
                        Q(number_of_floors__gt=self.request.GET.get('quantity-floor-min'), number_of_floors__lte=self.request.GET.get('quantity-floor-max')) |
                        Q(square_id__in=self.request.GET.getlist('square')) |
                        Q(rental_period=self.request.GET.get('time'))).distinct()

        queryset = queryset.annotate(sum_of_values=(Sum('rating__star')/Count('rating__star')))
        queryset = queryset.annotate(has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))
        return queryset


    def get_queryset(self):
        queryset = VehicleAd.objects.filter(rent=False)
        queryset = queryset.annotate(sum_of_values=(Sum('rating__star')/Count('rating__star')))
        queryset = queryset.annotate(has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))
        return queryset


class VehicleDetailView(AdDetailView):
    model = VehicleAd
    template_name = "vehicle/vehicle-single.html"


class VehicleCreateView(AdCreateView):
    model = VehicleAd
    form_class = VehicleMultiplyForm
    template_name = "vehicle/create-test.html"


class VehicleAdUpdateView(LockedView, UpdateView):
    model = VehicleAd
    form_class = VehicleMultiplyForm
    success_url = reverse_lazy('main')
    template_name = 'vehicle/update_test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_id'] = self.kwargs['pk']
        return context

    def get_form_kwargs(self):
        kwargs = super(VehicleAdUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'ad': self.object,
            'address': self.object.address,
        })
        return kwargs

    def form_valid(self, form):
        ad = form['ad'].save(commit=False)
        ad.save()
        photo = form['photo'].save(commit=False)
        photo.ad_id = ad
        photo.save()
        return redirect('main')

    def get_queryset(self):
        queryset = super(VehicleAdUpdateView, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset


# Service


class ServicesView(AdListView):
    model = ServiceAd
    template_name = "services/services.html"


class ServiceDetailView(DetailView):
    model = ServiceAd
    template_name = "services/services-single.html"


class ServiceCreateView(AdCreateView):
    model = ServiceAd
    form_class = ServiceAdMultiply
    template_name = "services/create-test.html"


class ServiceAdUpdateView(LockedView, UpdateView):
    model = ServiceAd
    form_class = ServiceAdMultiply
    success_url = reverse_lazy('main')
    template_name = 'vehicle/update_test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_id'] = self.kwargs['pk']
        return context

    def get_form_kwargs(self):
        kwargs = super(ServiceAdUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'ad': self.object,
            'address': self.object.address,
        })
        return kwargs

    def form_valid(self, form):
        ad = form['ad'].save(commit=False)
        ad.save()
        photo = form['photo'].save(commit=False)
        photo.ad_id = ad
        photo.save()
        return redirect('main')

    def get_queryset(self):
        queryset = super(ServiceAdUpdateView, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset


class AdDeleteForm(LockedView, DeleteView):
    model = Ad
    success_url = "/"

    template_name = "submit/delete_confirm.html"

    def get_queryset(self):
        queryset = super(AdDeleteForm, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset


class AddLocationView(CreateView):
    model = Location
    template_name = 'add/add_location.html'
    fields = (
        'city',
        'location',
    )

