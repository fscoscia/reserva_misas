from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from .views import (
    PersonViewSet,
    DisabledDateViewSet,
    ReservationView,
    ScheduleViewSet,
)

router = DefaultRouter()
router.register("schedules", ScheduleViewSet)
router.register("special-dates", DisabledDateViewSet)
router.register("persons", PersonViewSet)

urlpatterns = [
    path("reservations/", ReservationView.as_view()),
    path("", include(router.urls)),
]
