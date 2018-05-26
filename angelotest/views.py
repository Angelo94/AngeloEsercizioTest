from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import requests
import csv
import psycopg2
from angelotest.config import conn_str
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render

from angelotest.models import User

def login(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        email = request.POST['email']
		#UserAlreadyRegistered(User.objects.values_list('email','password'), email, password)
        if User.objects.filter(email=email,password=password).count() >= 1:
        	print("registrato")
        	return render(request, 'app/home.html', {'msg':'you are correctly logged in', 'username':name, 'email':email})
        else:
        	user = User(name=name,password=password,email=email)
        	user.save()
        	return render(request, 'app/login.html', {'msg':'user created, now just login', 'user':user})
    else:
        return render(request, 'app/login.html', {'msg':'please create a user or login if you are already registered'})