from django.urls import path
from forarmenians_app.views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('add-comment/<int:pk>/', AddCommentView.as_view(), name='add-comment'),
    path('add-like/<int:pk>/', AddLikeView.as_view(), name='add-like'),
    path('add-rating', AddStarRating.as_view(), name='add-rating'),
    path('add-location/', AddLocationView.as_view(), name='add-location'),

    path('abc/', ABCView.as_view(), name='abc'),
    path('abc/<int:pk>/', ABCDetailView.as_view(), name='abc-detail'),
    path('abc/create/', ABCAdCreate.as_view(), name='abc-create'),
    path('abc/update/<int:pk>/', ABCAdCreate.as_view(), name='abc-create'),

    path('cafe/', CafeView.as_view(), name='cafe'),
    path('cafe/<int:pk>/', CafeDetailView.as_view(), name='cafe-detail'),

    path('entertainments/', EntertainmentsView.as_view(), name='entertainments'),
    path('entertainment/<int:pk>/', EntertainmentsDetailView.as_view(), name='entertainments-detail'),

    path('events/', EventsView.as_view(), name='events'),
    path('event/<int:pk>/', EventsDetailView.as_view(), name='events-detail'),
    path('event/create/', EventCreateView.as_view(), name='event-create'),

    path('job/', JobView.as_view(), name='job'),
    path('job-catalog/vacancy/', JobCatalogVacancyView.as_view(), name='job-catalog-vacancy'),
    path('job/vacancy/<int:pk>/', JobVacancyDetailView.as_view(), name='job-detail-vacancy'),
    path('job-catalog/resume/', JobCatalogResumeView.as_view(), name='job-catalog-resume'),
    path('job/resume/<int:pk>/', JobResumeDetailView.as_view(), name='job-detail-resume'),
    path('job/create-vacancy/', JobVacancyCreateView.as_view(), name='job-detail-vacancy'),
    # path('job/create-resume/', JobResumeCreateView.as_view(), name='job-detail-resume'),

    path('market/', MarketAdView.as_view(), name='market'),
    path('market/create/', MarketCreateView.as_view(), name='market-create'),
    path('market/update/<int:pk>/', MarketCreateView.as_view(), name='market-update'),

    path('news/', NewsView.as_view(), name='news'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile-ads/', ProfileADCView.as_view(), name='profile-ads'),
    path('profile-wallet/', ProfileWalletView.as_view(), name='profile-wallet'),

    path('property/', PropertyView.as_view(), name='property'),
    path('property-filter/', PropertyFilterBuyView.as_view(), name='property-filter'),
    path('property-catalog/rent/', PropertyCatalogRentView.as_view(), name='property-catalog-rent'),
    path('property-catalog/buy/', PropertyCatalogBuyView.as_view(), name='property-catalog-buy'),
    path('property/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('property/create/', PropertyAdCreate.as_view(), name='property-create'),
    path('property/update/<int:pk>/', PropertyAdUpdateView.as_view(), name='property-update'),

    path('services', ServicesView.as_view(), name='services'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='services-detail'),
    path('services/create/', ServiceCreateView.as_view(), name='services-create'),
    path('services/update/<int:pk>/', ServiceAdUpdateView.as_view(), name='services-update'),

    path('useful/', UsefulView.as_view(), name='useful'),
    path('useful/detail/<int:pk>/', UsefulDetailView.as_view(), name='useful-detail'),

    path('choose-categories/', ChooceCategoriesView.as_view(), name='choose-categories'),
    path('vehicle/', VehicleView.as_view(), name='vehicle'),
    path('vehicle-catalog/', VehicleCatalogView.as_view(), name='vehicle-catalog'),
    path('vehicle-catalog/rent/', VehicleCatalogRentView.as_view(), name='vehicle-catalog-rent'),
    path('vehicle-filter', VehicleFilterView.as_view(), name='vehicle-filter'),
    path('vehicle/<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
    path('vehicle/create/', VehicleCreateView.as_view(), name='vehicle-create'),
    path('vehicle/update/<int:pk>/', VehicleAdUpdateView.as_view(), name='vehicle-update'),

    path('ad/delete/<int:pk>/', AdDeleteForm.as_view(), name='ad-delete'),

    # path('add-like/<int:pk>/', AddLikeView.as_view(), name='add-like'),
    # path('add-comment/<int:pk>/', AddCommentView.as_view(), name='add-comment'),


]

