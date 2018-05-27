# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
import os


class User(models.Model):
	userid = models.AutoField(primary_key = True)
	name = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	email = models.CharField(max_length=100)


class Booking(models.Model):
	bookid = models.AutoField(primary_key = True)
	userid = models.IntegerField()
	vehiclesid = models.IntegerField()
	startdate = models.DateField()
	enddate = models.DateField()
	place = models.CharField(max_length=100)

class Vehicles(models.Model):
	vehiclesid = models.AutoField(primary_key = True)
	code = models.CharField(max_length=10)
	model = models.CharField(max_length=100)
