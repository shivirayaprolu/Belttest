# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UserDB, TripSchedulesDB, JoinsDB

def index(request):
    return render(request, 'main_app/index.html')

def log_register(request):
    if request.method == "POST":
        print request.POST
        if request.POST["submit"] == "register":
            response = UserDB.objects.check_create(request.POST)
        elif request.POST["submit"] == "login":
            response = UserDB.objects.check_log(request.POST)
        if not response[0]:
            for message in response[1]:
                messages.error(request, message[1])
            return redirect('main_app:index')
        else:
            request.session['user'] = {
            "id": response[1].id,
            "name": response[1].name,
            "username": response[1].username,
            }
            return redirect('main_app:travels')
    return redirect('main_app:index')

def logout(request):
    request.session.clear()
    return redirect('main_app:index')

def travels(request):
    curr_id = request.session['user']['id']
    print("FFFFFFFFFFF")
    print curr_id
    yourdata = {
    "yourtrips": TripSchedulesDB.objects.filter(user=UserDB.objects.get(id=curr_id)),
    "otherstrips": TripSchedulesDB.objects.exclude(user=UserDB.objects.get(id=curr_id)),
    }
    print yourdata
    return render(request, 'main_app/travels.html', yourdata)

def addtrip(request):
    return render(request, 'main_app/addtrip.html')

def createtrip(request):
    if request.method == "POST":
        print request.POST
        #if request.POST["submit"] == "addtrip":
        current_user = UserDB.objects.get(id=request.session['user']['id'])
        response = TripSchedulesDB.objects.create_trip(request.POST, current_user)
    return redirect('main_app:travels')

def addtravel(request):
    if request.method == "POST":
        print ("SSSSSSSSS")
        print request.POST
    if request.POST["submit"] == "addtrip":
        response = TripSchedulesDB.objects.create_trip(request.POST)
    if not response[0]:
        for message in response[1]:
            messages.error(request, message[1])
        return redirect('main_app:travels')
    else:
        request.session['trip'] = {
        "id": response[1].id,
        "destination": response[1].destination,
        "description": response[1].description,
        }
        return redirect('main_app:travels')
    return render(request, 'main_app/addtravel.html')

def otherusertrip(request):
    pass

def yourtrip(request):
    yourdata = {
    "trips": TripSchedulesDB.objects.all(),
    }
    print yourdata
    return render(request, 'main_app/travels.html', yourdata)

def join(request, id):
    #return redirect('main_app:travels')
    pass

def destination(request, id):
    tripdata = {
    "dest": TripSchedulesDB.objects.filter(id=id),
    }
    print tripdata
    return render(request, 'main_app/destination.html', tripdata)

def home(request):
    return redirect('main_app:travels')
