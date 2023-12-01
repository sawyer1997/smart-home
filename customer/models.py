from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MinLengthValidator


class ServiceLocation(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apt_unit = models.IntegerField(
        default=1,
        verbose_name='AptUnit',
        help_text='Enter the Apartment unit of the building',
        validators=[MinValueValidator(1)],
    )
    street = models.CharField(
        max_length=50,
        verbose_name='Street Name',
        null=False,
    )
    state = models.CharField(
        max_length=20,
        verbose_name='State Name',
        null=False,
    )
    zipcode = models.CharField(
        default='00000',
        verbose_name='ZipCode',
        help_text='Enter the zipcode',
        validators=[MinLengthValidator(5)],
        null=False,
    )
    apt_name = models.CharField(
        max_length=100,
        verbose_name='AptName',
    )
    move_in_date = models.DateField(
        verbose_name='MoveInDate',
    )
    area = models.IntegerField(
        null=False,
        verbose_name='SquareFootage',
        validators=[MinValueValidator(100)],
    )
    bedroom = models.IntegerField(
        default=1,
        verbose_name='No of bedrooms',
        validators=[MinValueValidator(1)],
    )
    occupants = models.IntegerField(
        verbose_name='No of occupants',
    )

    def __str__(self):
        return f'{self.street}_{self.zipcode}_{self.state}_{self.id}'
