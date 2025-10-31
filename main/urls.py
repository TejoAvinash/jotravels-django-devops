from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reviews/', views.reviews, name='reviews'),
    path('about/', views.about, name='about'),
path('booking/', views.booking, name='booking'),

]
