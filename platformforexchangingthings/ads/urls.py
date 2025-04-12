from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import AdsListView

urlpatterns = [
    path('', AdsListView.as_view(), name='ads_list'),
    path('my_ads/', views.my_ads, name='my_ads'),
    path('create_ad/', views.create_ad, name='create_ad'),
    path('confirm_ad/<int:ad_id>/', views.confirm_ad, name='confirm_ad'),
    path('edit_ad/<int:ad_id>/', views.edit_ad, name='edit_ad'),
    path('delete_ad/<int:ad_id>/', views.delete_ad, name='delete_ad'),

    path('create_exchange_proposal/<int:ad_receiver>/',
         views.create_exchange_proposal, name='create_exchange_proposal'),
    path('sent_proposals/', views.sent_proposals, name='sent_proposals'),
    path('update_exchange_proposal/<int:proposal_id>/<str:status>/', views.update_exchange_proposal, name='update_exchange_proposal'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
