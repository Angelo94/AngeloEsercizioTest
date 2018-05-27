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
from angelotest.models import Booking
from angelotest.models import Vehicles

def login(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        email = request.POST['email']
		#UserAlreadyRegistered(User.objects.values_list('email','password'), email, password)
        if User.objects.filter(email=email,password=password).count() >= 1:
        	userID = User.objects.get(email=email,password=password)
        	userID = userID.userid
        	bookingList = mapBookings(userID)
        	vehiclesList = mapVehicles()
        	return render(request, 'app/home.html', {'userID':userID,'vehiclesList':vehiclesList,'BookingList':bookingList,'msg':'you are correctly logged in', 'username':name, 'email':email})
        else:
        	user = User(name=name,password=password,email=email)
        	user.save()
        	return HttpResponseRedirect('/')
        	#return render(request, 'app/login.html', {'msg':'user created, now just login', 'user':user})
    else:
        return render(request, 'app/login.html', {'msg':'please create a user or login if you are already registered'})

def bookVehicle(vehicleID,userid, enddate, startdate, place):
	booking = Booking(
		userid=userid,
		vehiclesid=vehicleID,
		startdate=startdate,
		enddate=enddate,
		place=place
	)
	booking.save()

	return "Booked"

def backToHome(request, userid):
	bookingList = mapBookings(userid)
	vehiclesList = mapVehicles()
	username = User.objects.get(userid=userid)
	username = username.name
	email = User.objects.get(userid=userid)
	email = email.email
	return render(request, 'app/home.html', {'userID':userid,'vehiclesList':vehiclesList,'BookingList':bookingList,'msg':'you are correctly logged in', 'username':username, 'email':email})

def vehiclesView(request, vehicleID, userid):
	msg = ""
	if request.method == 'POST':
		enddate = request.POST['enddate']
		startdate = request.POST['startdate']
		place = request.POST['place']
		msg = bookVehicle(vehicleID,userid, enddate, startdate, place)
	vehiclesData = Vehicles.objects.get(vehiclesid=vehicleID)
	vehiclesInfo = [vehiclesData.code, vehiclesData.model]
	vehicleBookedList = vehicleBooking(vehicleID,userid)
	return render(request, 'app/vehicledetails.html', {'userID':userid,'msg':msg, 'vehicleID':vehicleID,'VehicleBookedList':vehicleBookedList,'VehiclesInfo':vehiclesInfo})

def	vehicleBooking(vehicleID,userid):
	vehicleBookedList = []
	bookingList = Booking.objects.filter(vehiclesid=vehicleID, userid=userid)
	for booked in bookingList:
		model = Vehicles.objects.get(vehiclesid=booked.vehiclesid)
		vehicleBookedList.append({
			'bookid':booked.bookid,
			'userid':booked.userid,
			'vehiclesid':booked.vehiclesid,
			'model':model.model,
			'startdate':booked.startdate,
			'enddate':booked.enddate,
			'place':booked.place,
		})
	return vehicleBookedList


def mapBookings(userID):
	bookings = []
	bookedvehicles = Booking.objects.filter(userid=userID)
	for booking in bookedvehicles:
		model = Vehicles.objects.get(vehiclesid=booking.vehiclesid)
		bookings.append({
			'UserID':booking.userid,
			'Model':model.model,
			'StartDate':booking.startdate,
			'EndDate':booking.enddate,
			'Place':booking.place,
		})
	return bookings

def mapVehicles():
	vehicles = []
	getVehicles = Vehicles.objects.all()
	for vehicle in getVehicles:
		vehicles.append({
			'VehicleID':vehicle.vehiclesid,
			'Code':vehicle.code,
			'Model':vehicle.model,
		})
	return vehicles
