from rest_framework import serializers

from Theatre.models import (
    Play,
    TheatreHall,
    Performance,
    Actor,
    Genre,
    Reservation,
    Ticket,
)


class ActorForPlaySerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Actor
        fields = ("id", "full_name")


class ActorSerializer(serializers.ModelSerializer):
    plays = serializers.PrimaryKeyRelatedField(
        queryset=Play.objects.all(), many=True, required=False
    )

    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "plays")


class ActorListSerializer(ActorSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Actor
        fields = ("id", "full_name", "plays")


class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title")


class PlaySerializer(serializers.ModelSerializer):
    actors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Actor.objects.all(), required=False
    )
    genres = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all(), required=False
    )

    class Meta:
        model = Play
        fields = ("id", "title", "description", "actors", "genres", "image")


class PlayRetrieveSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    actors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
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
    play_title = serializers.CharField(source="play.title", read_only=True)
    theatre_hall_name = serializers.CharField(
        source="theatre_hall.name", read_only=True
    )

    class Meta:
        model = Performance
        fields = ("id", "show_time", "play_title", "theatre_hall_name")


class PerformanceListSerializer(serializers.ModelSerializer):
    play_title = serializers.CharField(source="play.title", read_only=True)
    theatre_hall_name = serializers.CharField(
        source="theatre_hall.name", read_only=True
    )
    available_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Performance
        fields = (
            "id",
            "play_title",
            "theatre_hall_name",
            "show_time",
            "available_seats",
        )


class TicketForPerformanceRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class PerformanceRetrieveSerializer(serializers.ModelSerializer):
    play = PlayListSerializer(read_only=True)
    theatre_hall = TheatreHallSerializer(read_only=True)
    available_seats = serializers.IntegerField(read_only=True)
    tickets = TicketForPerformanceRetrieveSerializer(many=True, read_only=True)

    class Meta:
        model = Performance
        fields = (
            "id",
            "play",
            "theatre_hall",
            "show_time",
            "available_seats",
            "tickets",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name", "plays")


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("created_at", "user")


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
    play_title = serializers.CharField(source="performance.play.title", read_only=True)
    theatre_hall_name = serializers.CharField(
        source="performance.theatre_hall.name", read_only=True
    )
    performance_show_time = serializers.DateTimeField(
        source="performance.show_time", read_only=True
    )
    user_email = serializers.CharField(source="reservation.user.email", read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "play_title",
            "theatre_hall_name",
            "performance_show_time",
            "user_email",
        )


class ReservationRetrieveSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    tickets = TicketListSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user_email", "tickets")


class ActorRetrieveSerializer(serializers.ModelSerializer):
    plays = PlayListSerializer(many=True, read_only=True)
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name", "plays")


class TicketRetrieveSerializer(serializers.ModelSerializer):
    play_title = serializers.CharField(source="performance.play.title", read_only=True)
    theatre_hall_name = serializers.CharField(
        source="performance.theatre_hall.name", read_only=True
    )
    performance_show_time = serializers.DateTimeField(
        source="performance.show_time", read_only=True
    )
    user_email = serializers.CharField(source="reservation.user.email", read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "play_title",
            "theatre_hall_name",
            "performance_show_time",
            "user_email",
        )
