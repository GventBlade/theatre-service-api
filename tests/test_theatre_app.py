import pytest
from django.utils import timezone
from django.db.models import F, Count
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

from Theatre.models import (
    Play,
    TheatreHall,
    Performance,
    Actor,
    Genre,
    Reservation,
    Ticket,
)
from Theatre.serializers import (
    PlaySerializer,
    PlayRetrieveSerializer,
    TheatreHallSerializer,
    PerformanceSerializer,
    PerformanceListSerializer,
    PerformanceRetrieveSerializer,
    ActorListSerializer,
    ActorRetrieveSerializer,
    GenreSerializer,
    TicketSerializer,
    TicketListSerializer,
    TicketRetrieveSerializer,
)


@pytest.fixture
def factory():
    return APIRequestFactory()


@pytest.fixture
def play_instance(db):
    return Play.objects.create(title="Hamlet", description="A Shakespeare tragedy")


@pytest.fixture
def theatre_hall_instance(db):
    return TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)


@pytest.fixture
def actor_instance(db, play_instance):
    actor = Actor.objects.create(first_name="Tom", last_name="Hanks")
    play_instance.actors.add(actor)
    return actor


@pytest.fixture
def genre_instance(db, play_instance):
    genre = Genre.objects.create(name="Tragedy")
    play_instance.genres.add(genre)
    return genre


@pytest.mark.django_db(transaction=True)
def test_play_serializer_create():
    data = {"title": "King Lear", "description": "Another Shakespeare tragedy"}
    serializer = PlaySerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    play = serializer.save()
    assert play.title == "King Lear"


@pytest.mark.django_db
def test_play_retrieve_serializer(play_instance, actor_instance, genre_instance):
    factory = APIRequestFactory()
    request = factory.get("/")
    serializer = PlayRetrieveSerializer(play_instance, context={"request": request})
    data = serializer.data

    assert data["title"] == "Hamlet"
    assert "Tragedy" in data["genres"]
    assert actor_instance.full_name in data["actors"]


@pytest.mark.django_db
def test_theatre_hall_serializer(theatre_hall_instance):
    serializer = TheatreHallSerializer(theatre_hall_instance)
    assert serializer.data["name"] == "Main Hall"


@pytest.mark.django_db
def test_performance_serializer(play_instance, theatre_hall_instance):
    perf = Performance.objects.create(
        play=play_instance, theatre_hall=theatre_hall_instance, show_time=timezone.now()
    )
    serializer = PerformanceSerializer(perf)
    assert serializer.data["play"] == play_instance.id
    assert serializer.data["theatre_hall"] == theatre_hall_instance.id


@pytest.mark.django_db(transaction=True)
def test_performance_list_serializer(play_instance, theatre_hall_instance):
    perf = Performance.objects.create(
        play=play_instance, theatre_hall=theatre_hall_instance, show_time=timezone.now()
    )
    User = get_user_model()
    user = User.objects.create_user(email="test@example.com", password="pass123")
    reservation = Reservation.objects.create(user=user)
    Ticket.objects.create(row=1, seat=1, performance=perf, reservation=reservation)

    perf_qs = (
        Performance.objects.select_related("play", "theatre_hall")
        .annotate(
            available_seats=F("theatre_hall__rows") * F("theatre_hall__seats_in_row")
            - Count("tickets")
        )
        .get(id=perf.id)
    )

    serializer = PerformanceListSerializer(perf_qs)
    data = serializer.data
    total_seats = theatre_hall_instance.rows * theatre_hall_instance.seats_in_row
    assert data["available_seats"] == total_seats - 1


@pytest.mark.django_db(transaction=True)
def test_performance_retrieve_serializer(play_instance, theatre_hall_instance):
    perf = Performance.objects.create(
        play=play_instance,
        theatre_hall=theatre_hall_instance,
        show_time="2025-08-25T19:00:00Z"
    )

    User = get_user_model()
    user = User.objects.create_user(email="u@test.com", password="pass123")
    reservation = user.reservation_set.create()
    Ticket.objects.create(row=1, seat=1, performance=perf, reservation=reservation)

    serializer = PerformanceRetrieveSerializer(perf)
    data = serializer.data

    assert data["play"]["title"] == "Hamlet"
    assert data["theatre_hall"]["name"] == "Main Hall"
    assert len(data["tickets"]) == 1
    ticket_data = data["tickets"][0]
    assert ticket_data["row"] == 1
    assert ticket_data["seat"] == 1


@pytest.mark.django_db(transaction=True)
def test_actor_list_and_retrieve_serializer(actor_instance):
    serializer = ActorListSerializer(actor_instance)
    assert serializer.data["full_name"] == "Tom Hanks"

    retrieve = ActorRetrieveSerializer(actor_instance)
    assert any(p["title"] == "Hamlet" for p in retrieve.data["plays"])


@pytest.mark.django_db(transaction=True)
def test_genre_serializer(genre_instance):
    serializer = GenreSerializer(genre_instance)
    assert serializer.data["name"] == "Tragedy"


@pytest.mark.django_db(transaction=True)
def test_ticket_serializers(play_instance, theatre_hall_instance):
    perf = Performance.objects.create(
        play=play_instance, theatre_hall=theatre_hall_instance, show_time=timezone.now()
    )
    User = get_user_model()
    user = User.objects.create_user(email="u@test.com", password="pass123")
    reservation = Reservation.objects.create(user=user)
    ticket = Ticket.objects.create(row=1, seat=1, performance=perf, reservation=reservation)

    s1 = TicketSerializer(ticket)
    assert s1.data["row"] == 1

    s2 = TicketListSerializer(ticket)
    assert s2.data["play_title"] == "Hamlet"
    assert s2.data["user_email"] == "u@test.com"

    s3 = TicketRetrieveSerializer(ticket)
    assert s3.data["theatre_hall_name"] == "Main Hall"
