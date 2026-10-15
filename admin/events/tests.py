import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from .models import Event, Registration


@pytest.fixture
def owner(db):
    return User.objects.create_user(username='owner', password='pass12345')


@pytest.fixture
def stranger(db):
    return User.objects.create_user(username='stranger', password='pass12345')


@pytest.fixture
def event(owner):
    return Event.objects.create(
        name='Python-митап',
        starts_at=timezone.now() + timezone.timedelta(days=7),
        location='Челябинск',
        capacity=10,
        organizer=owner,
    )


def test_stranger_gets_404_on_foreign_event(client, stranger, event):
    client.force_login(stranger)
    response = client.get(reverse('event_detail', args=[event.pk]))
    assert response.status_code == 404

def test_create_event_sets_organizer(client, owner):
    client.force_login(owner)
    data = {
        'name': 'Новое мероприятие',
        'description': '',
        'starts_at': '2026-12-01T18:00',
        'location': 'Онлайн',
        'capacity': 50,
        'status': 'draft',
    }
    response = client.post(reverse('event_create'), data)

    assert response.status_code == 302
    event = Event.objects.get(name='Новое мероприятие')
    assert event.organizer == owner

def test_anonymous_redirected_to_login(client, db):
    response = client.get(reverse('event_list'))
    assert response.status_code == 302
    assert '/accounts/login/' in response.url

def test_export_csv_contains_participants(client, owner, event):
    Registration.objects.create(event=event, name='Иван', email='ivan@example.com')
    client.force_login(owner)
    response = client.get(reverse('event_export', args=[event.pk]))
    assert response.status_code == 200
    assert response['Content-Type'].startswith('text/csv')
    content = response.content.decode('utf-8')
    assert 'ivan@example.com' in content