from django.contrib import admin
from .models import Schedule, Person, DisabledDate, Reservation


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("day", "time", "is_enabled")
    list_display_links = ("day", "time", "is_enabled")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "gov_id", "phone")
    list_display_links = ("first_name", "last_name")
    search_fields = ("first_name", "last_name", "gov_id", "email", "phone")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("date_time", "get_persons_total")
    list_display_links = ("date_time",)
    search_fields = ("persons__first_name", "persons__last_name", "persons__gov_id")
    list_filter = ("date_time",)
    filter_horizontal = ("persons",)

    def get_persons_total(self, obj):
        return obj.persons.count()

    get_persons_total.short_description = "Cant. Personas"


@admin.register(DisabledDate)
class DisabledDateAdmin(admin.ModelAdmin):
    list_display = ("date_time", "reason")
    list_display_links = ("date_time", "reason")
