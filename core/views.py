from rest_framework.throttling import AnonRateThrottle
from rest_framework import generics, viewsets, status, mixins
from rest_framework.response import Response
from .models import Person, Reservation, Schedule, DisabledDate
from .serializers import (
    PersonCreateSerializer,
    PersonSerializer,
    ScheduleSerializer,
    DisabledDateSerializer,
    ReservationWriteSerializer,
    ReservationReadSerializer,
)


class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Schedule.objects.filter(is_enabled=True)
    serializer_class = ScheduleSerializer


class DisabledDateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DisabledDate.objects.all()
    serializer_class = DisabledDateSerializer


class ReservationView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationWriteSerializer
    # throttle_classes = [AnonRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        response_serializer = ReservationReadSerializer(instance=instance)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class PersonViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin
):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = "gov_id"
    # throttle_classes = [AnonRateThrottle]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PersonSerializer
        else:
            return PersonCreateSerializer


class PersonCreateView(generics.CreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonCreateSerializer
