from rest_framework import serializers

from Theatre.models import (Play,
                            TheatreHall,
                            Performance,
                            Actor,
                            Genre,
                            Reservation,
                            Ticket
                            )


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title", "description", "image")


class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title")


class PlayRetrieveSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    image = serializers.SerializerMethodField()

    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors", "image")

    def get_image(self, obj):
        if obj.image:
            return self.context["request"].build_absolute_uri(obj.image.url)
        return None


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "play", "show_time")


class PerformanceListSerializer(serializers.ModelSerializer):
    play_title = serializers.CharField(source="play.title", read_only=True)
    theatre_hall_name = serializers.CharField(source="theatre_hall.name", read_only=True)
    available_seats_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Performance
        fields = ("id", "play_title", "theatre_hall_name", "show_time", "available_seats_count")

class PerformanceRetrieveSerializer(serializers.ModelSerializer):
    play = PlayListSerializer(read_only=True)
    theatre_hall = TheatreHallSerializer(read_only=True)
    total_seats = serializers.IntegerField(source="total_seats", read_only=True)
    available_seats_count = serializers.IntegerField(source="available_seats_count", read_only=True)
    available_seats = serializers.ListField(source="available_seats", read_only=True)

    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time", "total_seats",
                  "available_seats_count", "available_seats")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id","first_name","last_name","plays")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name", "plays")


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("created_at","user")


class ReservationListSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user_email")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat", "performance", "reservation")


class TicketListSerializer(serializers.ModelSerializer):
    performance_info = PerformanceListSerializer(source="performance", read_only=True)
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance_info")

class ReservationRetrieveSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    tickets = TicketListSerializer(many=True, read_only=True)
    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user_email", "tickets")

