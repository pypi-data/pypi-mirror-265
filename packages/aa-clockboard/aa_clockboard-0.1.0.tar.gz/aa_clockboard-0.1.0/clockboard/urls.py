from django.urls import path

from . import views

app_name = 'clockboard'


urlpatterns = [
    path('', views.index, name='index'),
    path('clocks/', views.dashboard, name='dashboard'),
    path('clocks/<int:clock_id>/reset/', views.reset_clock, name='reset_clock'),
    path('clocks/new/', views.new_clock, name='new_clock'),
]
