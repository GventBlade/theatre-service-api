from rest_framework import viewsets
from Theatre.models import (
    Play, TheatreHall, Performance, Actor, Genre, Reservation, Ticket
)
from Theatre.serializers import (
    PlaySerializer, PlayListSerializer, PlayRetrieveSerializer,
    TheatreHallSerializer,
    PerformanceSerializer, PerformanceListSerializer, PerformanceRetrieveSerializer,
    ActorSerializer, GenreSerializer,
    ReservationSerializer, ReservationListSerializer, ReservationRetrieveSerializer,
    TicketSerializer, TicketListSerializer
)

from permissions import IsAdminOrAuthenticatedOrReadOnly


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.prefetch_related("actors", "genres").all()
    permission_classes = (IsAdminOrAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        if self.action == "retrieve":
            return PlayRetrieveSerializer
        return PlaySerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = (IsAdminOrAuthenticatedOrReadOnly,)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("play", "theatre_hall")\
                                  .prefetch_related("ticket_set").all()

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceRetrieveSerializer
        return PerformanceSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.prefetch_related("plays").all()
    serializer_class = ActorSerializer
    permission_classes = (IsAdminOrAuthenticatedOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.prefetch_related("plays").all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrAuthenticatedOrReadOnly,)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related("user")\
                                  .prefetch_related("ticket_set__performance").all()
    permission_classes = (IsAdminOrAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        if self.action == "retrieve":
            return ReservationRetrieveSerializer
        return ReservationSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related("performance", "reservation").all()
    permission_classes = (IsAdminOrAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        return TicketSerializer
