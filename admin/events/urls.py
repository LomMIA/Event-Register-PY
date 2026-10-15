from django.urls import path
from django.views.generic import CreateView, DetailView, UpdateView

from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_update'),
]