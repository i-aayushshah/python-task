from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'sarbottam'

urlpatterns = [
    # Main pages
    path('', views.company_profile, name='company_profile'),
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('financial/', views.financial_data, name='financial_data'),
    path('achievements/', views.achievements, name='achievements'),
    path('price-history/', views.price_history, name='price_history'),
    path('predictions/', views.price_predictions, name='price_predictions'),

    # API endpoints
    path('api/company/', views.api_company_data, name='api_company_data'),
    path('api/news/', views.api_latest_news, name='api_latest_news'),
    path('api/price-history/', views.api_price_history, name='api_price_history'),
    path('api/predictions/', views.api_price_predictions, name='api_price_predictions'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
