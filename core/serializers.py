from datetime import datetime, timedelta
from django.db.models import fields
from django.db.models import Count, Q
from rest_framework import serializers
from .models import Schedule, Person, Reservation, DisabledDate
from django.utils import timezone

DAY_MAPPING = {
    6: Schedule.SUNDAY,
    0: Schedule.MONDAY,
    1: Schedule.TUESDAY,
    2: Schedule.WEDNESDAY,
    3: Schedule.THURSDAY,
    4: Schedule.FRIDAY,
    5: Schedule.SATURDAY,
}


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ("day", "time")


class DisabledDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisabledDate
        fields = ("id", "date_time", "reason")


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("id", "first_name", "last_name", "gov_id", "city")


class PersonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            "id",
            "first_name",
            "last_name",
            "gov_id",
            "phone",
            "email",
            "address",
            "city",
        )


class ReservationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "date_time", "persons")

    def validate_persons(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("Maximum 10 persons allowed.")
        return value

    def validate_date_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Date must be in the future.")
        _date = value.date()
        _time = value.time()
        if not Schedule.objects.filter(
            day=DAY_MAPPING[_date.weekday()], time=_time
        ).exists():
            raise serializers.ValidationError("Invalid date and/or time.")
        if DisabledDate.objects.filter(date_time__date=_date).exists():
            raise serializers.ValidationError("Selected date is not available.")
        return value

    def validate(self, attrs):
        errors = []

        _date = attrs["date_time"].date()
        _time = attrs["date_time"].time()
        schedule = Schedule.objects.get(day=DAY_MAPPING[_date.weekday()], time=_time)
        reservations = Reservation.objects.filter(
            date_time=attrs["date_time"]
        ).aggregate(total_persons=Count("persons"))
        person_qty = len(attrs["persons"])
        if reservations["total_persons"] + person_qty > schedule.persons_limit:
            errors.append("Not enough free places.")

        week_ago = attrs["date_time"] - timedelta(days=7)
        week_future = attrs["date_time"] + timedelta(days=7)
        if Reservation.objects.filter(
            date_time__gte=week_ago,
            date_time__lte=week_future,
            persons__in=attrs["persons"],
        ).exists():
            errors.append("Only one reservation per week is allowed.")
        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class ReservationReadSerializer(ReservationWriteSerializer):
    persons = PersonSerializer(many=True, read_only=True)

    class Meta(ReservationWriteSerializer.Meta):
        pass