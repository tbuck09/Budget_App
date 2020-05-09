from datetime import date

from django.db import models
from django.urls import reverse

# Create your models here.


class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=120)
    category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)

    def get_absolute_list_url(self):
        return reverse("transactions:Transaction", kwargs={"requested_id": self.id})
