# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt, re
VALIDREG = re.compile(r'^[a-zA-Z]*$')
DATEREG = re.compile(r'^[0-9]-[0-9]-[0-9]*$')

class UserDBManager(models.Manager):
    def hash_pass(self, password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def check_create(self, data):
        errors = []
        if len(data['name']) < 3:
            errors.append(['name', "Name must be at least three characters in length"])
        if len(data['username']) < 3:
            errors.append(['username', "User Name must be at least three characters in length"])
        if len(data['password']) < 8:
            errors.append(['password', "Password must be at lease eight characters in length"])
        if not data['password'] == data['confirmpass']:
            errors.append(['confirmpass', "Passwords do not match"])
        if errors:
            return [False, errors]
        else:
            curent_user = UserDB.objects.filter(username=data['username'])
            if curent_user:
                errors.append(['curent_user', "Unable to register, please use alternate information"])
                return [False, errors]
            newUser = UserDB(name=data['name'], username=data['username'])
            # hashed_pass = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            # print hashed_pass, "hashed password"
            newUser.hashpw = self.hash_pass(data['password'].encode())
            print newUser.hashpw
            newUser.save()
            print newUser
            return [True, newUser]

    def check_log(self, data):
        errors = []
        curent_user = UserDB.objects.filter(username=data['username'])
        if not curent_user:
            errors.append(['account', "UserName or Password incorrect"])
        elif not bcrypt.checkpw(data['password'].encode(), curent_user[0].hashpw.encode()):
            errors.append(['account', "UserName or Password incorrect"])
        if errors:
            return [False, errors]
        else:
            return [True, curent_user[0]]

class UserDB(models.Model):
    name = models.CharField(max_length=50, blank=False)
    username = models.CharField(max_length=50)
    hashpw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserDBManager()
    def __str__(self):
        return 'ID: %s | Name: %s | UserName: %s | Created: %s | Updated: %s' % (self.id, self.name, self.username, self.created_at, self.updated_at)

class TripDBManager(models.Manager):
    def create_trip(self, data, user):
        print(" I am in create_trip defination")
        newtrip = TripSchedulesDB(destination=data['destination'], description=data['description'], travelstartdate=data['travelstartdate'], travelenddate=data['travelenddate'], user=user)
        newtrip.save()
        print("After saving create trip")
        print newtrip
        return [True, newtrip]

class TripSchedulesDB(models.Model):
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    travelstartdate = models.DateField()
    travelenddate = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user=models.ForeignKey(UserDB, related_name="usertrip")

    objects = TripDBManager()
    def __str__(self):
        return 'ID: %s | Destination: %s | Description: %s | Travelstartdate: %s | Travelenddate: %s | Travelenddate: %s' % (self.id, self.destination, self.description, self.travelstartdate, self.travelenddate, self.user)

class JoinDBManager(models.Manager):
    pass

class JoinsDB(models.Model):
    user_join=models.ForeignKey(UserDB, related_name="user_join")
    trip_join=models.ForeignKey(TripSchedulesDB, related_name="trip_join")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = JoinDBManager()
