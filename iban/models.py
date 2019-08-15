from django.contrib.auth.models import User
from django.db import models

from localflavor.generic.models import IBANField
from localflavor.generic.countries.sepa import IBAN_SEPA_COUNTRIES


class IBAN(models.Model):
    user = models.ForeignKey(User, related_name='ibans', on_delete=models.CASCADE)
    number = IBANField(include_countries=IBAN_SEPA_COUNTRIES)
    creator = models.ForeignKey(User, related_name='created_ibans', on_delete=models.PROTECT)

    def __str__(self):
        return self.number
