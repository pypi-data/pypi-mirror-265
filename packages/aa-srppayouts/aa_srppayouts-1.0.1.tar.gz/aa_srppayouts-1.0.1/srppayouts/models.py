"""
App Models
Create your models in here
"""

# Django
from django.db import models
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Subquery, OuterRef
from django.db.models import F
from django.db.models.functions import Coalesce
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class General(models.Model):
    """Meta model for app permissions"""

    class Meta:
        """Meta definitions"""

        managed = False
        default_permissions = ()
        permissions = (("basic_access", "Can access this app"),
                       ("admin_access", "Can force to recalculate the table"),)

class Ship(models.Model):
    name = models.CharField(max_length=255, blank=True, unique=True)
    ship_id = models.IntegerField(default=0, unique=True)

    def __str__(self):
        return self.name

class Reimbursement(models.Model):
    index = models.IntegerField(default=0, unique=False)
    name = models.CharField(max_length=255, blank=True, unique=True)

    def __str__(self):
        return "#" + str(self.index) + " " + self.name

class Payout(models.Model):
    value = models.IntegerField(default=0, unique=False)
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name="cells", default=1)
    reimbursement = models.ForeignKey(Reimbursement, on_delete=models.CASCADE, related_name="cells", default=1)

    def __str__(self):
        return "(" + self.reimbursement.name + ") " + self.ship.name + ": " + format(self.value, ",") + " ISK"

def recalculate_matrix():
    ship_rows = Ship.objects.all().order_by("name")
    columns = Reimbursement.objects.all().order_by("index")
    matrix = []

    for row in ship_rows:
        if Payout.objects.filter(ship=row).count() > 0:
            row_data = [row]
            for column in columns:
                cell = Payout.objects.filter(ship=row, reimbursement=column).first()
                row_data.append(cell)
            matrix.append(row_data)

    cache.set('matrix', matrix, None)

def calculate_temp_matrix(query):

    if query:
        ship_rows = Ship.objects.filter(name__icontains=query).order_by("name")
        columns = Reimbursement.objects.all().order_by("index")
        matrix = []

        for row in ship_rows:
            if Payout.objects.filter(ship=row).count() > 0:
                row_data = [row]
                for column in columns:
                    cell = Payout.objects.filter(ship=row, reimbursement=column).first()
                    row_data.append(cell)
                matrix.append(row_data)

        return matrix
    else:
        ship_rows = Ship.objects.all().order_by("name")
        columns = Reimbursement.objects.all().order_by("index")
        matrix = []

        for row in ship_rows:
            if Payout.objects.filter(ship=row).count() > 0:
                row_data = [row]
                for column in columns:
                    cell = Payout.objects.filter(ship=row, reimbursement=column).first()
                    row_data.append(cell)
                matrix.append(row_data)
        
        return matrix


## Payout Receiver

@receiver(post_save, sender=Payout)
def payout_post_save(sender, instance, **kwargs):
    recalculate_matrix()

@receiver(post_delete, sender=Payout)
def payout_post_delete(sender, instance, **kwargs):
    recalculate_matrix()

## Reimbursement Receiver

@receiver(post_save, sender=Reimbursement)
def reimbursement_post_save(sender, instance, **kwargs):
    recalculate_matrix()

@receiver(post_delete, sender=Reimbursement)
def reimbursement_post_delete(sender, instance, **kwargs):
    recalculate_matrix()

## Ship Receiver

@receiver(post_save, sender=Ship)
def ship_post_save(sender, instance, **kwargs):
    recalculate_matrix()

@receiver(post_delete, sender=Ship)
def ship_post_delete(sender, instance, **kwargs):
    recalculate_matrix()
