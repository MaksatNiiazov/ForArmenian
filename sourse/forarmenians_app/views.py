from django.shortcuts import render
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = "mainPage/index.html"


class ABCView(TemplateView):
    template_name = "abc/abc.html"


class ABSDetailView(TemplateView):
    template_name = "abc/abc-single.html"


class CafeView(TemplateView):
    template_name = "cafe/cafe.html"


class CafeDetailView(TemplateView):
    template_name = "cafe/cafe-single.html"


class EntertainmentsView(TemplateView):
    template_name = "entertainments/entertainments.html"


class EntertainmentsDetailView(TemplateView):
    template_name = "entertainments/entertainments-single.html"


class EventsView(TemplateView):
    template_name = "events/events.html"


class EventsDetailView(TemplateView):
    template_name = "events/events-single.html"


class JobView(TemplateView):
    template_name = "job/job.html"


class JobCatalogView(TemplateView):
    template_name = "job/job-catalog.html"


class JobDetailView(TemplateView):
    template_name = "job/job-single.html"


class MarketView(TemplateView):
    template_name = "market/market.html"


class NewsView(TemplateView):
    template_name = "news/news.html"


class NewsDetailView(TemplateView):
    template_name = "news/news-single.html"


class ProfileView(TemplateView):
    template_name = "profile/profile.html"


class ProfileADCView(TemplateView):
    template_name = "profile/profile-ads.html"


class ProfileWalletView(TemplateView):
    template_name = "profile/profile-wallet.html"


class PropertyView(TemplateView):
    template_name = "property/property.html"


class PropertyCatalogView(TemplateView):
    template_name = "property/property-catalog.html"


class PropertyDetailView(TemplateView):
    template_name = "property/property-single.html"


class ServicesView(TemplateView):
    template_name = "services/services.html"


class ServiceDetailView(TemplateView):
    template_name = "services/services-single.html"


class UsefulView(TemplateView):
    template_name = "useful/useful.html"


class UsefulDetailView(TemplateView):
    template_name = "useful/useful-single.html"


class ChooceCategoriesView(TemplateView):
    template_name = "vehicle/choose-categories.html"


class VehicleView(TemplateView):
    template_name = "vehicle/vehicle.html"


class VehicleCatalogView(TemplateView):
    template_name = "vehicle/vehicle-catalog.html"


class VehicleDetailView(TemplateView):
    template_name = "vehicle/vehicle-single.html"


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
