from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, OuterRef, Exists, Q
from django.utils import timezone
from django.db.models.functions import Coalesce
from django.http import HttpResponse, QueryDict
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from forarmenians_app.forms import *
from forarmenians_app.models import *
from user_auth.models import User
from chat.models import Room
import uuid


class LockedView(LoginRequiredMixin):
    login_url = "login"


class AddCommentView(View):

    def post(self, request, pk):
        form = CommentForm(request.POST)
        user = User.objects.get(email=self.request.user)
        ad = Ad.objects.get(id=self.kwargs['pk'])

        if form.is_valid():

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


class UserStarRating(View):

    def post(self, request):
        form = UserRatingForm(request.POST)
        if form.is_valid():
            ad = Ad.objects.get(id=self.request.POST.get("ad")),

            UserRating.objects.update_or_create(
                user_by=self.request.user,
                user_id=1,
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class AddStarRating(View):

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                user=self.request.user,
                ad_id=int(request.POST.get("ad")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class MainPageView(ListView):
    template_name = "mainPage/index.html"
    model = PropertyAd

    def get_queryset(self):
        return PropertyAd.objects.all()[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_anonymous:
            context['services'] = ServiceAd.objects.all()[:8]
            context['jobs'] = JobVacancy.objects.all()[:6]
            context['abc'] = ABCAd.objects.all()[:7]
            context['entertainments'] = EntertainmentAd.objects.all()[:3]
            context['useful_resources'] = UsefulResources.objects.all()[:3]
            context['news'] = News.objects.all()[:4]
            context['events'] = EventAd.objects.all()[:3]
        else:
            context['services'] = ServiceAd.objects.all()[:8].annotate(
                has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user))).annotate(
                sum_of_values=Coalesce(Sum('rating__star') / Count('rating__star'), 0))
            context['jobs'] = JobVacancy.objects.all()[:6].annotate(
                has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user))).annotate(
                sum_of_values=Coalesce(Sum('rating__star') / Count('rating__star'), 0))
            context['abc'] = ABCAd.objects.all()[:7].annotate(
                has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user))).annotate(
                sum_of_values=Coalesce(Sum('rating__star') / Count('rating__star'), 0))
            context['cafes'] = CafeAd.objects.all()[:3].annotate(
                has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user))).annotate(
                sum_of_values=Coalesce(Sum('rating__star') / Count('rating__star'), 0))
            context['entertainments'] = EntertainmentAd.objects.all()[:3].annotate(
                has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user))).annotate(
                sum_of_values=Coalesce(Sum('rating__star') / Count('rating__star'), 0))
            context['useful_resources'] = UsefulResources.objects.all()[:3].annotate(
                has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user))).annotate(
                sum_of_values=Coalesce(Sum('rating__star') / Count('rating__star'), 0))
            context['news'] = News.objects.all()[:4].annotate(
                has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))
            context['events'] = EventAd.objects.all()[:3].annotate(
                has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user))).annotate(
                sum_of_values=Coalesce(Sum('rating__star') / Count('rating__star'), 0))
        return context


class AdListView(ListView):
    model = None
    template_name = None
    paginate_by = 20
    ordering = None
    ordering_options = ['id', '-id']
    default_ordering = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(sum_of_values=Coalesce(Sum('rating__star') / Count('rating__star'), 0))
        if not self.request.user.is_anonymous:
            queryset = queryset.annotate(
                has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))

        sort = self.request.GET.get('sort', None)
        if sort in self.ordering_options:
            self.ordering = sort
        else:
            self.ordering = self.default_ordering

        queryset = queryset.order_by(self.ordering)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['ordering_options'] = self.ordering_options

        context['current_ordering'] = self.ordering

        query_dict = QueryDict(mutable=True)
        query_dict.update(self.request.GET)

        context['query_dict'] = query_dict

        return context


class AdDetailView(DetailView):
    model = None
    template_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = AdComment.objects.filter(ad_id=self.object.id)
        context['ads'] = Ad.objects.filter(created_by=self.object.created_by)
        try:
            a, b = self.object.address.location.location.split(',')
            context['lat'] = a
            context['lng'] = b

        except:
            print('ex')

        if not self.request.user.is_anonymous:
            context['like'] = AdLike.objects.filter(ad_id=self.kwargs['pk'], user=self.request.user)
            context['star_form'] = RatingForm
            context['rating'] = self.get_star()
            context['avg'] = self.get_avg()
            context['user_rating'] = self.get_star_user()
            context['user_avg'] = self.get_avg_user()
            context['user_rating_count'] = UserRating.objects.filter(user_id=self.object.created_by.id).all().count()

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
            return 0  # нужно исправить на что то нормальное

    def get_avg(self):
        review_avg = Rating.objects.filter(ad=self.object).all()
        summ = 0
        for i in review_avg:
            summ += i.star.value
        count = Rating.objects.filter(ad=self.object).count()
        if count == 0:
            count = 1
        return summ / count

    def get_star_user(self):
        if UserRating.objects.filter(user_by=self.request.user, user=self.object.created_by):
            a = UserRating.objects.filter(user_by=self.request.user, user=self.object.created_by).first().star.value
            # return a
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
            return 0  # нужно исправить на что то нормальное

    def get_avg_user(self):
        review_avg = UserRating.objects.filter(user_id=self.object.created_by.id).all()
        summ = 0
        for i in review_avg:
            summ += i.star.value
        count = UserRating.objects.filter(user_id=self.object.created_by.id).count()
        if count == 0:
            count = 1
        return summ / count


class AdCreateView(LockedView, CreateView):
    model = None
    form_class = None
    template_name = None

    def form_invalid(self, form):
        print(form.errors)

    def form_valid(self, form):
        user = User.objects.get(email=self.request.user)
        ad = form['ad'].save(commit=False)
        ad.created_by = user
        if 'country__address-country' in self.request.POST:
            country = AdCountry.objects.get_or_create(country=self.request.POST.get('country__address-country'))[0]
            state = AdState.objects.get_or_create(state=self.request.POST.get('state__address-state'))[0]
            address_ = self.request.POST.get('address__address-address')
            location = None
            if 'coordinates' in self.request.POST:
                location = Location.objects.get_or_create(location=self.request.POST.get('coordinates'),
                                                          city=self.request.POST.get('city'))[0]
            address = AdAddress.objects.get_or_create(
                state=state,
                country=country,
                address=address_,
                location=location,
            )[0]
            ad.address_id = address.id

        ad.save()
        if self.request.FILES.getlist('photo-img'):
            print(self.request.FILES.getlist('photo-img'))
            for _ in self.request.FILES.getlist('photo-img'):
                photo = AdImage.objects.get_or_create(img=_, ad_id=ad.id)[0] or None
                photo.save()
        return redirect('main')


class AdUpdateView(LockedView, UpdateView):
    model = None
    form_class = None
    success_url = None
    template_name = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(instance={
            'ad': self.object,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = AdImage.objects.filter(ad_id=self.object.id)
        return context

    def form_valid(self, form):
        ad = form['ad'].save(commit=False)
        if 'country__address-country' in self.request.POST:
            country = AdCountry.objects.get_or_create(country=self.request.POST.get('country__address-country'))[0]
            state = AdState.objects.get_or_create(state=self.request.POST.get('state__address-state'))[0]
            address = self.request.POST.get('address__address-address')
            location = Location.objects.get_or_create(city=self.request.POST.get('city'),
                                                      location=self.request.POST.get('coordinates'))[0]
            ad.address = \
                AdAddress.objects.get_or_create(country=country, state=state, address=address, location=location)[0]

        ad.save()

        if self.request.FILES.get('photo-img'):
            for image in AdImage.objects.filter(ad_id=ad.id):
                image.delete()

            for img in self.request.FILES.getlist('photo-img'):
                AdImage.objects.create(img=img, ad_id=ad.id)

        return redirect('main')


# ABC


class ABCView(AdListView):
    model = ABCAd
    template_name = "abc/abc.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        distinct_countries = AdAddress.objects.values('country').distinct()
        context['locations'] = AdAddress.objects.filter(country__in=distinct_countries).distinct()
        context['categories'] = ABCCategory.objects.all()
        context['selected_location'] = self.request.GET.get('location')
        context['selected_categories'] = self.request.GET.getlist('categories')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(address_id=location)

        selected_categories = self.request.GET.getlist('categories')
        if selected_categories:
            queryset = queryset.filter(category__in=selected_categories)

        min_price = self.request.GET.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        max_price = self.request.GET.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        search_query = self.request.GET.get('keyword')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset


class ABCDetailView(AdDetailView):
    model = ABCAd
    template_name = "abc/abc-single.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['popular_ads'] = Ad.objects.all().order_by('?')[:6].exclude(self.object)
        # context['similar'] = Ad.objects.all().order_by('?')[:6].exclude(self.object)
        return context


class ABCAdCreate(AdCreateView):
    model = ABCAd
    form_class = ABCMultiplyForm
    template_name = 'abc/abc_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ABCCategory.objects.all()
        context['services'] = ABCService.objects.filter(abc_id=self.object.id)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        ad = form['ad'].save(commit=False)
        services = self.request.POST.getlist('services')
        prices = self.request.POST.getlist('prices')

        for i in range(len(services)):
            ABCService.objects.get_or_create(abc=ad, service=services[i], price=prices[i])

        return response


class ABCAdUpdateView(AdUpdateView):
    model = ABCAd
    form_class = ABCMultiplyForm
    success_url = reverse_lazy('main')
    template_name = 'abc/abc_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ABCCategory.objects.all()
        context['services'] = ABCService.objects.filter(abc_id=self.object.id)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        ad = self.object
        services = self.request.POST.getlist('services')
        prices = self.request.POST.getlist('prices')

        if self.request.POST.get('services'):
            for i in self.object.abs_services.all():
                i.delete()
            for i in range(len(services)):
                ABCService.objects.get_or_create(abc=ad, service=services[i], price=prices[i])

        return response


class ABCAdDeleteView(DeleteView):
    model = ABCAd
    success_url = reverse_lazy('main')




# Café


class CafeView(AdListView):
    model = CafeAd
    template_name = "cafe/cafe.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        distinct_countries = AdAddress.objects.values('country').distinct()

        context['categories'] = CafeType.objects.all()
        context['features'] = CafeSpecificType.objects.all()
        context['kitchens'] = CafeKitchenType.objects.all()
        context['locations'] = AdAddress.objects.filter(country__in=distinct_countries)
        context['selected_location'] = self.request.GET.get('location')
        context['selected_categories'] = list(map(int, self.request.GET.getlist('categories')))
        context['selected_kitchens'] = self.request.GET.getlist('kitchens')
        context['selected_features'] = self.request.GET.getlist('features')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(address_id=location)

        search_query = self.request.GET.get('keyword')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        open_now = self.request.GET.get('open')
        if open_now:
            local_time = timezone.now().time()
            queryset = queryset.filter(start_time__lte=local_time)

        if min_price and max_price:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        selected_kitchens = self.request.GET.getlist('kitchens')
        if selected_kitchens:
            queryset = queryset.filter(kitchens__kitchen__kitchen__in=selected_kitchens)

        selected_features = self.request.GET.getlist('features')
        if selected_features:
            queryset = queryset.filter(specifics__specific__specific__in=selected_features)

        selected_categories = self.request.GET.getlist('categories')
        if selected_categories:
            queryset = queryset.filter(type__in=selected_categories)

        return queryset


class CafeDetailView(AdDetailView):
    model = CafeAd
    template_name = "cafe/cafe-single.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        similar_cafes = CafeAd.objects.filter(Q(type=self.object.type) |
                                              Q(kitchens__in=self.object.kitchens.all())).exclude(pk=self.object.pk)[:5]

        context['similar'] = similar_cafes

        return context


class CafeCreateView(AdCreateView):
    model = CafeAd
    form_class = CafeMultiplyForm
    template_name = 'cafe/cafe_create.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = CafeType.objects.all()
        context['kitchens'] = CafeKitchenType.objects.filter(cafes__cafe=self.object)
        context['specifics'] = CafeSpecificType.objects.filter(cafes__cafe=self.object)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        ad = form['ad'].save(commit=False)
        print(self.request.POST.getlist('kitchen-kitchen'))
        print(self.request.POST.getlist('specific-specific'))
        for kitchen in self.request.POST.getlist('kitchen-kitchen'):
            k = CafeKitchenType.objects.get_or_create(kitchen=kitchen)[0]
            CafeKitchen.objects.get_or_create(kitchen=k, cafe=ad)
        for specific in self.request.POST.getlist('specific-specific'):
            s = CafeSpecificType.objects.get_or_create(specific=specific)[0]
            CafeSpecific.objects.get_or_create(specific=s, cafe=ad)

        return response


class CafeUpdateView(AdUpdateView):
    model = CafeAd
    form_class = CafeMultiplyForm
    success_url = reverse_lazy('main')
    template_name = 'cafe/cafe_update.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = CafeType.objects.all()
        context['kitchens'] = CafeKitchenType.objects.filter(cafes__cafe=self.object)
        context['specifics'] = CafeSpecificType.objects.filter(cafes__cafe=self.object)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        ad = self.object
        specifics = self.request.POST.getlist('specific-specific')
        kitchens = self.request.POST.getlist('kitchen-kitchen')

        if self.request.POST.get('specific-specific'):
            for i in self.object.specifics.all():
                i.delete()
            for i in specifics:
                var = CafeSpecificType.objects.get_or_create(specific=i)[0]
                CafeSpecific.objects.get_or_create(cafe=ad, specific=var)

        if self.request.POST.get('kitchen-kitchen'):
            for i in self.object.kitchens.all():
                i.delete()
            for i in kitchens:
                var = CafeKitchenType.objects.get_or_create(kitchen=i)[0]
                CafeKitchen.objects.get_or_create(cafe=ad, kitchen=var)

        return response


# Entertainments


class EntertainmentsView(AdListView):
    model = EntertainmentAd
    template_name = "entertainments/entertainments.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        distinct_countries = AdAddress.objects.values('country').distinct()
        context['locations'] = AdAddress.objects.filter(country__in=distinct_countries)
        context['selected_location'] = self.request.GET.get('location')
        context['categories'] = EntertainmentType.objects.all()
        context['selected_categories'] = self.request.GET.getlist('categories')

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(address_id=location)

        open_now = self.request.GET.get('open')
        if open_now:
            local_time = timezone.now().time()
            queryset = queryset.filter(start_time__lte=local_time)

        search_query = self.request.GET.get('keyword')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        selected_categories = self.request.GET.getlist('categories')
        if selected_categories:
            queryset = queryset.filter(type__in=selected_categories)

        return queryset


class EntertainmentsDetailView(AdDetailView):
    model = EntertainmentAd
    template_name = "entertainments/entertainments-single.html"


class EntertainmentsCreateView(AdCreateView):
    model = EntertainmentAd
    form_class = EntertainmentsMultiplyForm
    template_name = 'entertainments/entertainments_create.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = EntertainmentType.objects.all()
        return context


class EntertainmentsUpdateView(AdUpdateView):
    model = EntertainmentAd
    form_class = EntertainmentsMultiplyForm
    success_url = reverse_lazy('main')
    template_name = 'entertainments/entertainments_update.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = EntertainmentType.objects.all()
        return context


# Events


class EventsView(AdListView):
    model = EventAd
    template_name = "events/events.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        distinct_countries = AdAddress.objects.values('country').distinct()
        context['locations'] = AdAddress.objects.filter(country__in=distinct_countries)
        context['selected_location'] = self.request.GET.get('location')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        from_date = self.request.GET.get('fromDate')
        to_date = self.request.GET.get('toDate')

        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(address_id=location)

        if to_date:
            queryset = queryset.filter(date__lte=to_date)
        if from_date:
            queryset = queryset.filter(date__gte=from_date)

        return queryset


class EventListView(EventsView):
    template_name = 'events/event_list.html'


class EventsDetailView(AdDetailView):
    model = EventAd
    template_name = "events/events-single.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        similar_events = EventAd.objects.filter(Q(category=self.object.category)).exclude(pk=self.object.pk)[:5]
        context['similar_events'] = similar_events

        return context


class EventCreateView(AdCreateView):
    model = EventAd
    form_class = EventAdMultiply
    template_name = 'events/event_create.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EventCategory.objects.all()
        return context


class EventUpdateView(AdUpdateView):
    model = EventAd
    form_class = EventAdMultiply
    success_url = reverse_lazy('main')
    template_name = 'events/event_update.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EventCategory.objects.all()
        return context


# Job


class JobView(TemplateView):
    template_name = "job/job.html"


class JobBaseList(AdListView):
    model = None
    template_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['educations'] = JobEducation.objects.all()
        context['graphics'] = JobWorkGraphic.objects.all()
        return context


class JobCatalogResumeView(JobBaseList):
    model = JobResume
    template_name = "job/job-catalog-resume.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        min_price = self.request.GET.get('price_min')
        if min_price:
            queryset = queryset.filter(salary_from__gt=min_price)

        max_price = self.request.GET.get('price_max')
        if max_price:
            queryset = queryset.filter(salary_to__lte=max_price)

        education = self.request.GET.getlist('education')
        if education:
            queryset = queryset.filter(education_id__in=education)

        graphic = self.request.GET.getlist('graphic')
        if graphic:
            queryset = queryset.filter(work_graphic_id__in=graphic)

        search_query = self.request.GET.get('keyword')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        queryset = queryset.annotate(sum_of_values=Coalesce(Sum('rating__star') / Count('rating__star'), 0))
        queryset = queryset.annotate(
            has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))
        return queryset


class JobResumeDetailView(AdDetailView):
    model = JobResume
    template_name = "job/job-single-resume.html"


class JobCatalogVacancyView(JobBaseList):
    model = JobVacancy
    template_name = "job/job-catalog-vacancy.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        min_price = self.request.GET.get('price_min')
        if min_price:
            queryset = queryset.filter(salary_from__gt=min_price)

        max_price = self.request.GET.get('price_max')
        if max_price:
            queryset = queryset.filter(salary_to__lte=max_price)

        education = self.request.GET.getlist('education')
        if education:
            queryset = queryset.filter(education_id__in=education)

        graphic = self.request.GET.getlist('graphic')
        if graphic:
            queryset = queryset.filter(work_graphic_id__in=graphic)

        search_query = self.request.GET.get('keyword')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        queryset = queryset.annotate(sum_of_values=Coalesce(Sum('rating__star') / Count('rating__star'), 0))
        if not self.request.user.is_anonymous:
            queryset = queryset.annotate(
                has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))
        return queryset


class JobVacancyDetailView(AdDetailView):
    model = JobVacancy
    template_name = "job/job-single-vacancy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = JobLanguageSkill.objects.filter(job_ad=self.object.pk)
        context['similar'] = JobAd.objects.all().exclude(pk=self.object.pk)
        return context


class JobVacancyCreateView(AdCreateView):
    model = JobVacancy
    form_class = JobVacancyMultiplyForm
    template_name = 'job/job-create-vacancy.html'
    success_url = reverse_lazy('job')


class JobResumeCreateView(AdCreateView):
    model = JobResume
    form_class = JobResumeMultiplyForm
    template_name = 'job/job-create-resume.html'
    success_url = reverse_lazy('job')

    def get_context_data(self, **kwargs):
        context = super(JobResumeCreateView, self).get_context_data()
        context['work_grapfics'] = JobWorkGraphic.objects.all()
        context['educations'] = JobEducation.objects.all()
        context['fops'] = JobFrequencyOfPayment.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        ad = form['ad'].save(commit=False)
        language = self.request.POST.getlist('languages-language')
        level = self.request.POST.getlist('languages-level')
        work_place = self.request.POST.getlist('experience-work_place')
        month = self.request.POST.getlist('experience-month')
        experience = self.request.POST.getlist('experience-experience')
        skills = self.request.POST.getlist('key_skills-skill')

        for i in range(len(language)):
            JobLanguageSkill.objects.get_or_create(job_ad=ad, language=language[i], level=level[i])

        for i in range(len(work_place)):
            JobWorkExperience.objects.get_or_create(job_ad=ad, work_place=work_place[i], month=month[i],
                                                    experience=experience[i])
        for skill in skills:
            JobKeySkills.objects.get_or_create(job_ad=ad, skill=skill)
        return response


class JobResumeUpdateView(AdUpdateView):
    model = JobResume
    form_class = JobResumeMultiplyForm
    success_url = reverse_lazy('main')
    template_name = 'job/job-update-resume.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['work_grapfics'] = JobWorkGraphic.objects.all()
        context['educations'] = JobEducation.objects.all()
        context['fops'] = JobFrequencyOfPayment.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        ad = self.object
        language = self.request.POST.getlist('languages-language')
        level = self.request.POST.getlist('languages-level')
        work_place = self.request.POST.getlist('experience-work_place')
        month = self.request.POST.getlist('experience-month')
        experience = self.request.POST.getlist('experience-experience')
        skills = self.request.POST.getlist('key_skills-skill')

        if self.request.POST.get('languages-language'):
            for i in JobLanguageSkill.objects.filter(job_ad=ad):
                i.delete()
            for i in range(len(language)):
                JobLanguageSkill.objects.get_or_create(job_ad=ad, language=language[i], level=level[i])
        if self.request.POST.get('experience-work_place'):
            for i in JobWorkExperience.objects.filter(job_ad=ad):
                i.delete()
            for i in range(len(work_place)):
                JobWorkExperience.objects.get_or_create(job_ad=ad, work_place=work_place[i], month=month[i],
                                                        experience=experience[i])
        if self.request.POST.get('key_skills-skill'):
            for i in JobKeySkills.objects.filter(job_ad=ad):
                i.delete()
            for skill in skills:
                JobKeySkills.objects.get_or_create(job_ad=ad, skill=skill)

        return response


class JobVacancyUpdateView(AdUpdateView):
    model = JobVacancy
    form_class = JobVacancyMultiplyForm
    success_url = reverse_lazy('main')
    template_name = 'job/job-update-vacancy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['work_grapfics'] = JobWorkGraphic.objects.all()
        context['educations'] = JobEducation.objects.all()
        context['fops'] = JobFrequencyOfPayment.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        ad = self.object
        language = self.request.POST.getlist('languages-language')
        level = self.request.POST.getlist('languages-level')
        skills = self.request.POST.getlist('key_skills-skill')

        if self.request.POST.get('languages-language'):
            for i in JobLanguageSkill.objects.filter(job_ad=ad):
                i.delete()
            for i in range(len(language)):
                JobLanguageSkill.objects.get_or_create(job_ad=ad, language=language[i], level=level[i])

        if self.request.POST.get('key_skills-skill'):
            for i in JobKeySkills.objects.filter(job_ad=ad):
                i.delete()
            for skill in skills:
                JobKeySkills.objects.get_or_create(job_ad=ad, skill=skill)

        return response


# Market


class MarketAdView(AdListView):
    model = MarketAd
    template_name = "market/market.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = MarketCategory.objects.all()
        context['selected_categories'] = self.request.GET.getlist('categories')
        context['selected_conditions'] = self.request.GET.getlist('condition_of_goods')
        distinct_countries = AdAddress.objects.values('country').distinct()
        context['locations'] = AdAddress.objects.filter(country__in=distinct_countries).distinct()
        context['selected_location'] = self.request.GET.get('location')

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')

        if price_min:
            queryset = queryset.filter(price__gt=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        categories = self.request.GET.getlist('categories')
        if categories:
            queryset = queryset.filter(category_id__in=categories)

        conditions = self.request.GET.getlist('condition_of_goods')
        if len(conditions) == 1:
            queryset = queryset.filter(is_new=True) if int(conditions[0]) else queryset.filter(is_new=False)

        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(address_id=location)

        search_query = self.request.GET.get('keyword')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset




class MarketDetail(AdDetailView):
    model = MarketAd
    template_name = 'market/market-single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paypal_dict = {
            "business": "sb-ij2ps25177360@business.example.com",
            "amount": self.object.price,
            "item_name": self.object.pk,
            "invoice": str(uuid.uuid4()),
            "notify_url": self.request.build_absolute_uri(reverse('paypal-ipn')),
            "return": self.request.build_absolute_uri(reverse('market-detail', kwargs={'pk': self.object.pk})),
            "cancel_return": self.request.build_absolute_uri(reverse('market-detail', kwargs={'pk': self.object.pk})),
        }

        context['paypal_form'] = PaymentForm(initial=paypal_dict)

        return context


class MarketCreateView(AdCreateView):
    model = MarketAd
    form_class = MarketAdMultiply
    template_name = 'market/market_create.html'

    def get_context_data(self, **kwargs):
        context = super(MarketCreateView, self).get_context_data(**kwargs)
        context['stickers'] = MarketSticker.objects.all()
        context['categories'] = MarketCategory.objects.all()
        return context


class MarketUpdateView(AdUpdateView):
    model = MarketAd
    form_class = MarketAdMultiply
    success_url = reverse_lazy('main')
    template_name = 'market/market_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stickers'] = MarketSticker.objects.all()
        context['categories'] = MarketCategory.objects.all()
        return context


# News


class NewsView(ListView):
    model = News
    template_name = "news/news.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('keyword')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        if not self.request.user.is_anonymous:
            queryset = queryset.annotate(has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'),
                                                                               user=self.request.user)))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        important_q = News.objects.all()
        if not self.request.user.is_anonymous:
            important_q = important_q.annotate(has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'),
                                                                                     user=self.request.user)))
        context['important_news'] = important_q

        return context


class NewsDetailView(AdDetailView):
    model = News
    template_name = "news/news-single.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        similar_news = News.objects.filter(Q(tags__in=self.object.tags.all()) |
                                           Q(category=self.object.category)) \
                           .exclude(pk=self.object.pk)[:5]
        context['similar_news'] = similar_news
        return context


class NewsCreateView(CreateView, LockedView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_create.html'

    def form_invalid(self, form):
        print(form.errors)

    def form_valid(self, form):
        user = User.objects.get(email=self.request.user)
        news = News.objects.create(
            created_by=user,

            title=form.title,
            category_id=form.category,
            description=form.description,
            photo=form.photo,
            news_source=form.news_source,
            link=form.link,
            important=form.important
        )

        return redirect('main')


# Profile


class ProfileView(DetailView):
    model = User
    template_name = "profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = PropertyAd.objects.filter(created_by=self.object, is_active=True)
        context['vehicles'] = VehicleAd.objects.filter(created_by=self.object, is_active=True)
        context['jobs_v'] = JobVacancy.objects.filter(created_by=self.object, is_active=True)
        context['jobs_r'] = JobResume.objects.filter(created_by=self.object, is_active=True)
        context['markets'] = MarketAd.objects.filter(created_by=self.object, is_active=True)
        context['services'] = ServiceAd.objects.filter(created_by=self.object, is_active=True)
        context['cafes'] = CafeAd.objects.filter(created_by=self.object, is_active=True)
        context['abcs'] = ABCAd.objects.filter(created_by=self.object, is_active=True)
        context['usefuls'] = UsefulResources.objects.filter(created_by=self.object, is_active=True)
        context['events'] = EventAd.objects.filter(created_by=self.object, is_active=True)
        context['entreteiments'] = EntertainmentAd.objects.filter(created_by=self.object, is_active=True)
        context['messages'] = Room.objects.filter(chats__user=self.object)
        context['ratings'] = Rating.objects.filter(user=self.object)
        context['likes'] = AdLike.objects.filter(user=self.object.id)
        return context


class ProfileMessages(ListView):
    model = Room
    template_name = 'profile/profile-messages.html'
    context_object_name = 'messages'

    def get_queryset(self):

        return Room.objects.filter(chats__user=self.request.user)


class ProfileReviews(ListView):
    model = Rating
    template_name = 'profile/profile-reviews.html'
    context_object_name = 'ratings'

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)


class ProfileSettings(TemplateView):
    template_name = 'profile/profile-settings.html'


class ProfileADCView(ProfileView):
    template_name = "profile/profile-ads.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = PropertyAd.objects.filter(created_by=self.object, is_active=True)
        context['vehicles'] = VehicleAd.objects.filter(created_by=self.object, is_active=True)
        context['jobs_v'] = JobVacancy.objects.filter(created_by=self.object, is_active=True)
        context['jobs_r'] = JobResume.objects.filter(created_by=self.object, is_active=True)
        context['markets'] = MarketAd.objects.filter(created_by=self.object, is_active=True)
        context['services'] = ServiceAd.objects.filter(created_by=self.object, is_active=True)
        context['cafes'] = CafeAd.objects.filter(created_by=self.object, is_active=True)
        context['abcs'] = ABCAd.objects.filter(created_by=self.object, is_active=True)
        context['usefuls'] = UsefulResources.objects.filter(created_by=self.object, is_active=True)
        context['events'] = EventAd.objects.filter(created_by=self.object, is_active=True)
        context['entreteiments'] = EntertainmentAd.objects.filter(created_by=self.object, is_active=True)
        return context


class ProfileWalletView(TemplateView):
    template_name = "profile/profile-wallet.html"


class UserUpdate(View):

    def post(self, request):
        user = User.objects.get(id=self.request.user.id)
        user.first_name = request.POST.get('name')
        user.last_name = request.POST.get('last-name')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone')
        user.avatar = request.FILES.get('avatar') or user.avatar
        user.save()

        return redirect(request.META.get('HTTP_REFERER'))


# Property


class PropertyView(TemplateView):
    template_name = "property/property.html"


class PropertyCatalogRentView(AdListView):
    model = PropertyAd
    template_name = "property/property-catalog.html"

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


class PropertyCatalogBuyView(AdListView):
    model = PropertyAd
    template_name = "property/property-catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat'] = True
        context['categories'] = PropertyCategory.objects.all()
        context['condition'] = PropertyCondition.objects.all()
        context['rental_period'] = PropertyRentalPeriod.objects.all()
        context['square'] = PropertySquare.objects.all()
        context['bedrooms'] = PropertyBedrooms.objects.all().order_by('bedrooms')
        context['bathrooms'] = PropertyBathrooms.objects.all().order_by('bathroom')

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        property_type = self.request.GET.getlist('type_property')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        conditions = self.request.GET.getlist('condition')
        categories = self.request.GET.getlist('category')
        rooms = self.request.GET.getlist('rooms')
        bathrooms = self.request.GET.getlist('bathrooms')
        floor_min = self.request.GET.get('floor_min')
        floor_max = self.request.GET.get('floor_max')
        quantity_floor_min = self.request.GET.get('quantity_floor_min')
        quantity_floor_max = self.request.GET.get('quantity_floor_max')
        square = self.request.GET.getlist('square')
        rental_period = self.request.GET.get('time')

        if property_type:
            queryset = queryset.filter(property_type_id__in=property_type)
        if price_min:
            queryset = queryset.filter(price__gt=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if conditions:
            queryset = queryset.filter(condition_id__in=conditions)
        if categories:
            queryset = queryset.filter(category_id__in=categories)
        if rooms:
            queryset = queryset.filter(bedrooms_id__in=rooms)
        if bathrooms:
            queryset = queryset.filter(bathrooms_id__in=bathrooms)
        if floor_min:
            queryset = queryset.filter(floor__gt=floor_min)
        if floor_max:
            queryset = queryset.filter(floor__lte=floor_max)
        if quantity_floor_min:
            queryset = queryset.filter(number_of_floors__gt=quantity_floor_min)
        if quantity_floor_max:
            queryset = queryset.filter(number_of_floors__lte=quantity_floor_max)
        if square:
            queryset = queryset.filter(square_id__in=square)
        if rental_period:
            queryset = queryset.filter(rental_period=rental_period)

        search_query = self.request.GET.get('keyword')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        queryset = queryset.annotate(sum_of_values=Coalesce(Sum('rating__star') / Count('rating__star'), 0))
        if not self.request.user.is_anonymous:

            queryset = queryset.annotate(
                has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))
        return queryset


class PropertyDetailView(AdDetailView):
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
    template_name = 'property/property_create.html'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = PropertyType.objects.all()
        context['categories'] = PropertyCategory.objects.all()
        context['condition'] = PropertyCondition.objects.all()
        context['rental_period'] = PropertyRentalPeriod.objects.all()
        context['square'] = PropertySquare.objects.all()
        context['bedrooms'] = PropertyBedrooms.objects.all()
        context['bathrooms'] = PropertyBathrooms.objects.all()

        return context


class PropertyAdUpdateView(AdUpdateView):
    model = PropertyAd
    form_class = PropertyMultiplyForm
    success_url = reverse_lazy('main')
    template_name = 'property/property_update_test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = PropertyType.objects.all()
        context['categories'] = PropertyCategory.objects.all()
        context['condition'] = PropertyCondition.objects.all()
        context['rental_period'] = PropertyRentalPeriod.objects.all()
        context['square'] = PropertySquare.objects.all()
        context['bedrooms'] = PropertyBedrooms.objects.all()
        context['bathrooms'] = PropertyBathrooms.objects.all()

        return context


# Useful


class UsefulView(AdListView):
    model = UsefulResources
    template_name = "useful/useful.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('keyword')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset


class UsefulDetailView(AdDetailView):
    template_name = "useful/useful-single.html"
    model = UsefulResources


class UsefulCreateView(AdCreateView):
    model = UsefulResources
    template_name = 'useful/useful_create.html'
    form_class = UsefulResourcesMultiply


class UsefulUpdateView(AdUpdateView):
    model = UsefulResources
    template_name = 'useful/useful_update.html'
    form_class = UsefulResourcesMultiply
    success_url = reverse_lazy('main')


# Vehicle


class ChooceCategoriesView(TemplateView):
    template_name = "vehicle/choose-categories.html"


class VehicleView(TemplateView):
    template_name = "vehicle/vehicle.html"


class VehicleBaseView(AdListView):
    model = VehicleAd
    template_name = None

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = VehicleAd.objects.filter(rent=False)
        queryset = queryset.annotate(sum_of_values=Coalesce(Sum('rating__star') / Count('rating__star'), 0))
        if not self.request.user.is_anonymous:
            queryset = queryset.annotate(
                has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = VehicleType.objects.all()
        context['conditions'] = VehicleCondition.objects.all()

        return context


class VehicleFilterView(VehicleBaseView):
    template_name = "vehicle/vehicle-catalog.html"

    def get_queryset(self):
        queryset = VehicleAd.objects.filter(
            Q(type_id__in=self.request.GET.getlist('cars')) |
            Q(price__gt=self.request.GET.get('price-min'), price__lte=self.request.GET.get('price-max')) |
            Q(rent__in=self.request.GET.getlist('buy')) |
            Q(condition_id__in=self.request.GET.getlist('condition')) |
            Q(year__gt=self.request.GET.get('registration-year-min'),
              year__lte=self.request.GET.get('registration-year-max')) |
            Q(mileage__gt=self.request.GET.get('mileage-min'), mileage__lte=self.request.GET.get('mileage-max')) |
            Q(engine_volume__gt=self.request.GET.get('engine-capacity-min'),
              engine_volume__lte=self.request.GET.get('engine-capacity-max'))).distinct()

        queryset = queryset.annotate(sum_of_values=Coalesce(Sum('rating__star') / Count('rating__star'), 0))
        if not self.request.user.is_anonymous:
            queryset = queryset.annotate(
                has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))
        return queryset


class VehicleBuyCatalogView(VehicleBaseView):
    template_name = "vehicle/vehicle-catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rent'] = False
        context['selected_conditions'] = self.request.GET.getlist('condition')
        context['selected_types'] = self.request.GET.getlist('cars')
        distinct_countries = AdAddress.objects.values('country').distinct()
        context['locations'] = AdAddress.objects.filter(country__in=distinct_countries).distinct()
        context['selected_location'] = self.request.GET.get('location')
        return context

    def get_queryset(self):
        queryset = VehicleAd.objects.all()
        cars = self.request.GET.getlist('cars')
        if cars:
            queryset = queryset.filter(type_id__in=cars)

        price_min = self.request.GET.get('price_min')
        if price_min:
            queryset = queryset.filter(price__gt=price_min)

        price_max = self.request.GET.get('price_max')
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        buy = self.request.GET.getlist('buy')
        if buy:
            queryset = queryset.filter(rent__in=buy)

        condition = self.request.GET.getlist('condition')
        if condition:
            queryset = queryset.filter(condition_id__in=condition)

        registration_year_min = self.request.GET.get('registration_year_min')
        if registration_year_min:
            queryset = queryset.filter(year__gt=registration_year_min)

        registration_year_max = self.request.GET.get('registration_year_max')
        if registration_year_max:
            queryset = queryset.filter(year__lte=registration_year_max)

        mileage_min = self.request.GET.get('mileage_min')
        if mileage_min:
            queryset = queryset.filter(mileage__gt=mileage_min)

        mileage_max = self.request.GET.get('mileage_max')
        if mileage_max:
            queryset = queryset.filter(mileage__lte=mileage_max)

        engine_capacity_min = self.request.GET.get('engine_capacity_min')
        if engine_capacity_min:
            queryset = queryset.filter(engine_volume__gt=engine_capacity_min)

        engine_capacity_max = self.request.GET.get('engine_capacity_max')
        if engine_capacity_max:
            queryset = queryset.filter(engine_volume__lte=engine_capacity_max)

        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(address_id=location)

        search_query = self.request.GET.get('keyword')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        queryset = queryset.annotate(sum_of_values=Coalesce(Sum('rating__star') / Count('rating__star'), 0))
        queryset = queryset.annotate(
            has_like=Exists(AdLike.objects.filter(ad_id=OuterRef('pk'), user=self.request.user)))
        return queryset



class VehicleRentCatalogView(VehicleBaseView):
    template_name = "vehicle/vehicle-catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rent'] = True
        return context


class VehicleDetailView(AdDetailView):
    model = VehicleAd
    template_name = "vehicle/vehicle-single.html"


class VehicleCreateView(AdCreateView):
    model = VehicleAd
    form_class = VehicleMultiplyForm
    template_name = "vehicle/vehicle_create.html"


class VehicleAdUpdateView(AdUpdateView):
    model = VehicleAd
    form_class = VehicleMultiplyForm
    success_url = reverse_lazy('main')
    template_name = 'vehicle/vehicle_update.html'


# Service


class ServicesView(AdListView):
    model = ServiceAd
    template_name = "services/services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = ServiceCategory.objects.all()
        context['selected_categories'] = self.request.GET.getlist('categories')
        distinct_countries = AdAddress.objects.values('country').distinct()
        context['locations'] = AdAddress.objects.filter(country__in=distinct_countries).distinct()
        context['selected_location'] = self.request.GET.get('location')

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(address_id=location)

        search_query = self.request.GET.get('keyword')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        categories = self.request.GET.getlist('categories')
        if categories:
            queryset = queryset.filter(category_id__in=categories)

        open_now = self.request.GET.get('open')
        if open_now:
            local_time = timezone.now().time()
            queryset = queryset.filter(start_time__lte=local_time)

        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')

        if price_min:
            queryset = queryset.filter(price__gt=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        return queryset


class ServiceDetailView(AdDetailView):
    model = ServiceAd
    template_name = "services/services-single.html"


class ServiceCreateView(AdCreateView):
    model = ServiceAd
    form_class = ServiceAdMultiply
    template_name = "services/services_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.all()
        return context


class ServiceAdUpdateView(AdUpdateView):
    model = ServiceAd
    form_class = ServiceAdMultiply
    success_url = reverse_lazy('main')
    template_name = 'services/service_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.all()
        return context


class AdDeleteForm(LockedView, DeleteView):
    model = Ad
    success_url = reverse_lazy('main')

    template_name = "submit/delete_confirm.html"

    def get_queryset(self):
        queryset = super(AdDeleteForm, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset


class UserAdsView(DetailView):
    model = User
    template_name = 'profile/user-ads.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = PropertyAd.objects.filter(created_by=self.kwargs['pk'], is_active=True)
        context['vehicles'] = VehicleAd.objects.filter(created_by=self.kwargs['pk'], is_active=True)
        context['jobs_v'] = JobVacancy.objects.filter(created_by=self.kwargs['pk'], is_active=True)
        context['jobs_r'] = JobResume.objects.filter(created_by=self.kwargs['pk'], is_active=True)
        context['markets'] = MarketAd.objects.filter(created_by=self.kwargs['pk'], is_active=True)
        context['services'] = ServiceAd.objects.filter(created_by=self.kwargs['pk'], is_active=True)
        context['cafes'] = CafeAd.objects.filter(created_by=self.kwargs['pk'], is_active=True)
        context['abcs'] = ABCAd.objects.filter(created_by=self.kwargs['pk'], is_active=True)
        context['usefuls'] = UsefulResources.objects.filter(created_by=self.kwargs['pk'], is_active=True)
        context['events'] = EventAd.objects.filter(created_by=self.kwargs['pk'], is_active=True)
        context['entreteiments'] = EntertainmentAd.objects.filter(created_by=self.kwargs['pk'], is_active=True)

        return context


class TermOfUseView(TemplateView):
    template_name = 'submit/terms_of_use.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'submit/privacy_policy.html'
