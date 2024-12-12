from django.contrib import admin
from django.urls import path, include
from .views import DailyArticleAPIView, ScraperAPIView

urlpatterns = [
    path('', DailyArticleAPIView.as_view(), name='dailyarticles'),
    path('articles/', DailyArticleAPIView.as_view(), name='dailyarticles'),
    path('scrape/', ScraperAPIView.as_view(), name='scrape_api'),
]