from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PlayViewSet,
    TheatreHallViewSet,
    PerformanceViewSet,
    ActorViewSet,
    GenreViewSet,
    ReservationViewSet,
    TicketViewSet,
)

router = DefaultRouter()
router.register("plays", PlayViewSet)
router.register("theatre-halls", TheatreHallViewSet)
router.register("performances", PerformanceViewSet, basename="performance")
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("reservations", ReservationViewSet, basename="reservation")
router.register("tickets", TicketViewSet, basename="ticket")

urlpatterns = [
    path("", include(router.urls)),
]