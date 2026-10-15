import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import EventForm
from .models import Event


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
    template_name = 'events/event_detail.html'

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)


@login_required
def event_export_csv(request, pk):
    event = get_object_or_404(Event, pk=pk, organizer=request.user)

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="event_{event.pk}_participants.csv"'
    response.write('\ufeff')

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Имя', 'Email', 'Статус', 'Дата регистрации'])

    for reg in event.registrations.all():
        writer.writerow([
            reg.name,
            reg.email,
            reg.get_status_display(),
            reg.created_at.strftime('%d.%m.%Y %H:%M'),
        ])

    return response