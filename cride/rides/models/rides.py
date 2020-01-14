"""Rides model."""

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel


class Rides(CRideModel):
    """Ride model."""

    # Los Rides son lo mas importante de la aplicacion.
    # No queremos perder ninguno aunque se borren los usuarios.
    offered_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    offered_in = models.ForeignKey('circles.Circle', on_delete=models.SET_NULL, null=True)

    passengers = models.ManyToManyField('users.User', related_name='passengers')

    available_seats = models.PositiveSmallIntegerField(default=1)
    comments = models.TextField(blank=True)

    departure_location = models.CharField(max_length=255)
    departure_date = models.DateTimeField()
    arraival_location = models.CharField(max_length=255)
    arraival_date = models.DateTimeField()

    raiting = models.FloatField(null=True)

    is_active = models.BooleanField(
        'active status',
        default=True,
        help_text='Used for disabling the ride or making it as finished.'
    )

    def __str__(self):
        """Return ride details."""
        return '{_from} to {to} | {day} {i_time} - {f_time}'.format(
            _from=self.departure_location,
            to=self.arraival_location,
            day=self.departure_date..strftime('%a %d %b'),
            i_time=self.departure_date.strftime('%I:%M: %p'),
            f_time=self.arraival_date.strftime('%I:%M: %p')
        )
