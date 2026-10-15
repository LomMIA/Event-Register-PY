from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView
from .models import Event
from .forms import EventForm
from django.urls import reverse



@login_required
def event_list(request):
    events = Event.objects.filter(organizer=request.user)
    return render(request, 'events/event_list.html', {'events': events})


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class EventCreateView(LoginRequiredMixin, CreateView):
    form_class = EventForm
    template_name = 'events/event_form.html'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UpdateView):
    form_class = EventForm
    template_name = 'events/event_form.html'

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)


class EventDetailView(LoginRequiredMixin, DetailView):
    form_class = EventForm
    template_name = 'events/event_detail.html'

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)