from django.db import models
from datetime import time


class Schedule(models.Model):
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    DAY_CHOICES = (
        (SUNDAY, "Domingo"),
        (MONDAY, "Lunes"),
        (TUESDAY, "Martes"),
        (WEDNESDAY, "Miércoles"),
        (THURSDAY, "Jueves"),
        (FRIDAY, "Viernes"),
        (SATURDAY, "Sábado"),
    )
    day = models.IntegerField("Día", choices=DAY_CHOICES)
    time = models.TimeField("Hora", default=time(19, 0))
    persons_limit = models.PositiveSmallIntegerField(
        "Cant. máx. de personas", default=100
    )
    is_enabled = models.BooleanField("Activado", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"
        unique_together = (("day", "time"),)

    def __str__(self) -> str:
        return f"{self.get_day_display()} {self.time}"


class Person(models.Model):
    first_name = models.CharField("Nombre", max_length=100, db_index=True)
    last_name = models.CharField("Apellido", max_length=100, db_index=True)
    gov_id = models.CharField("Cédula", max_length=20, unique=True)
    phone = models.CharField("Teléfono", max_length=20)
    email = models.EmailField("Email")
    address = models.TextField("Dirección")
    city = models.CharField("Ciudad", max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name


class Reservation(models.Model):
    date_time = models.DateTimeField("Fecha y Hora", db_index=True)
    persons = models.ManyToManyField(Person, related_name="reservations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self) -> str:
        return str(self.date_time)


class DisabledDate(models.Model):
    date_time = models.DateTimeField("Fecha y Hora", unique=True)
    reason = models.CharField("Motivo", max_length=250)

    class Meta:
        verbose_name = "Fecha Especial"
        verbose_name_plural = "Fechas Especiales"

    @property
    def _date(self):
        return self.date_time.date()

    def __str__(self) -> str:
        return str(self.date_time)