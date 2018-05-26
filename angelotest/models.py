# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
import os


class User(models.Model):
	userid = models.AutoField(primary_key = True)
	name = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
