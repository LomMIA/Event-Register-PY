from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Event


@login_required
def event_list(request):
    events = Event.objects.filter(organizer=request.user)
    return render(request, 'events/event_list.html', {'events': events})


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')