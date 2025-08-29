from django.db.models import F, Count
from rest_framework import viewsets
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
    PlayListSerializer,
    PlayRetrieveSerializer,
    TheatreHallSerializer,
    PerformanceListSerializer,
    PerformanceRetrieveSerializer,
    GenreSerializer,
    PerformanceSerializer,
    ReservationSerializer,
    TicketSerializer,
    TicketListSerializer,
    ActorListSerializer,
    ActorRetrieveSerializer,
    ActorSerializer,
    TicketRetrieveSerializer,
)

from permissions import IsAdminOrReadOnly, IsAdminOrOwner


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all().prefetch_related("actors", "genres")
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        if self.action == "retrieve":
            return PlayRetrieveSerializer
        return PlaySerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = (IsAdminOrReadOnly,)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceRetrieveSerializer
        return PerformanceSerializer

    def get_queryset(self):
        queryset = Performance.objects.all()

        if self.action == "list":
            queryset = queryset.select_related("play", "theatre_hall").annotate(
                available_seats=F("theatre_hall__rows")
                * F("theatre_hall__seats_in_row")
                - Count("tickets")
            )
        elif self.action == "retrieve":
            queryset = queryset.select_related("play", "theatre_hall").prefetch_related(
                "tickets__reservation"
            )
        return queryset


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.prefetch_related("plays").all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return ActorListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return ActorSerializer
        return ActorRetrieveSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.prefetch_related("plays").all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()

    permission_classes = (IsAdminOrOwner,)

    def get_queryset(self):
        queryset = self.queryset.select_related("user").prefetch_related(
            "tickets__performance__play", "tickets__performance__theatre_hall"
        )
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        return ReservationSerializer


class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrOwner,)

    def get_queryset(self):
        queryset = Ticket.objects.select_related(
            "performance__play", "performance__theatre_hall", "reservation__user"
        )
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(reservation__user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        if self.action == "retrieve":
            return TicketRetrieveSerializer
        return TicketSerializer
