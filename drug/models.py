from django.db import models
from django.utils import timezone
from account.models import User, Costumer, Worker
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, timedelta
import datetime
import pprint
# Create your models here.
class Storage_condition(models.Model):
    name        = models.CharField(max_length=100)
    additional  = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Helber(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Hemjee(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Savalgaa(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Drug_type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Drug_detail(models.Model):
    drug_name               = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.drug_name

class Drug(models.Model):
    drug_code               = models.CharField(max_length=100)
    drug_name               = models.CharField(max_length=300)
    instructions            = models.CharField(max_length=300)
    serial_number           = models.CharField(max_length=100)
    producted_date          = models.DateField(default=timezone.now)
    hadgalah_hugatsaa       = models.CharField(max_length=100)
    uildver_ner             = models.CharField(max_length=100)
    sanuulga                = models.CharField(max_length=1000)
    drug_type               = models.ForeignKey(Drug_type, on_delete=models.SET_NULL, null=True, blank=True)
    savalgaa                = models.ForeignKey(Savalgaa, on_delete=models.SET_NULL, null=True, blank=True)
    hemjee                  = models.ForeignKey(Hemjee, on_delete=models.SET_NULL, null=True, blank=True)
    helber                  = models.ForeignKey(Helber, on_delete=models.SET_NULL, null=True, blank=True)
    storage_condition       = models.ForeignKey(Storage_condition, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.drug_name

class Other_staff(models.Model):
    name                = models.CharField(max_length=500)
    hemjee              = models.CharField(max_length=50)
    uildver             = models.CharField(max_length=200)
    producted_date      = models.DateField(default=timezone.now)
    hadgalah_hugatsaa   = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Partner(models.Model):
    name            = models.CharField(max_length=200)
    address         = models.CharField(max_length=200)
    phone           = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Order(models.Model):
    ordered_date    = models.DateField(default=timezone.now)
    irraved_date    = models.DateField(null=True, blank=True)
    is_irraved      = models.BooleanField(default=False)
    worker          = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True)

class Ordered_drug(models.Model):
    order       = models.ForeignKey(Order, on_delete=models.CASCADE)
    drug        = models.ForeignKey(Drug, on_delete=models.SET_NULL, null=True, blank=True)
    qty         = models.IntegerField()

    def __str__(self):
        return str(self.qty)

class Ordered_staff(models.Model):
    order       = models.ForeignKey(Order, on_delete=models.CASCADE)
    staff       = models.ForeignKey(Other_staff, on_delete=models.SET_NULL, null=True, blank=True)
    qty         = models.IntegerField()

class Drug_resource(models.Model):
    drug                = models.OneToOneField(Drug, on_delete=models.SET_NULL, null=True, blank=True)
    qty                 = models.IntegerField()
    last_transaction    = models.DateField(default=timezone.now)

class Staff_resource(models.Model):
    staff               = models.OneToOneField(Other_staff, on_delete=models.SET_NULL, null=True, blank=True)
    qty                 = models.IntegerField()
    last_transaction    = models.DateField(default=timezone.now)

class Onosh(models.Model):
    category    = models.CharField(max_length=200, null=True, blank=True)
    disc        = models.CharField(max_length=400, null=True, blank=True)
    code        = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.disc

class Emchilgee(models.Model):
    start_date      = models.DateField(default=timezone.now)
    end_date        = models.DateField(default=timezone.now)
    worker          = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True)
    costumer        = models.ForeignKey(Costumer, on_delete=models.SET_NULL, null=True, blank=True)
    onosh           = models.ForeignKey(Onosh, on_delete=models.SET_NULL, null=True, blank=True)
    created_date    = models.DateField(default=timezone.now)

    def is_started(self):
        return self.start_date <= date.today()

    def is_done(self):
        return self.end_date < date.today()

    def has_review(self):
         rsp = get_object_or_404(Doctor_review, emchilgee = self.id)
         return rsp
    def count_days(self):
        result = self.end_date + timedelta(days=1) - self.start_date
        return int(result.days)

class Days_of_emchilgee(models.Model):
    emchilgee               = models.ForeignKey(Emchilgee, on_delete=models.CASCADE, default=1)
    day                     = models.DateField(default=timezone.now)
    is_done                 = models.BooleanField(default=False)

    def __str__(self):
        return str(self.emchilgee.id)

class Emchilgee_list(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class History(models.Model):
    costumer        = models.ForeignKey(Costumer, on_delete=models.SET_NULL, null=True, blank=True)
    doctor          = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True)
    created_date    = models.DateField(default=timezone.now)
    disc            = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.costumer

class Drug_important(models.Model):
    emchilgee               = models.ForeignKey(Emchilgee, on_delete=models.CASCADE, default=1)
    emchilgee_list          = models.ForeignKey(Emchilgee_list, on_delete=models.SET_NULL, null=True, blank=True)
    name                    = models.ForeignKey(Drug_detail, on_delete=models.SET_NULL, null=True, blank=True)
    shirheg                 = models.IntegerField(default=0)
    is_ordered              = models.BooleanField('ordered_status', default=False)

    def __str__(self):
        return self.name.name

class Drug_order_status(models.Model):
    name    = models.CharField(max_length=100)
    about   = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Drug_order(models.Model):
    name            = models.ForeignKey(Drug_detail, on_delete=models.SET_NULL, null=True, blank=True)
    number          = models.IntegerField(default=0)
    ordered_date    = models.DateField(default=timezone.now)
    recived_date    = models.DateField(null=True, blank=True)
    nurse           = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.date

class Doctor_review(models.Model):
    emchilgee       = models.IntegerField(default=0)
    doctor          = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True)
    review          = models.IntegerField(default=1)

class Costumer_review(models.Model):
    emchilgee       = models.IntegerField(default=0)
    costumer        = models.ForeignKey(Costumer, on_delete=models.SET_NULL, null=True, blank=True)
    review          = models.IntegerField(default=1)
