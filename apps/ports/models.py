# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
import bcrypt
import re
from datetime import *
import uuid
import os
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import requests, json
from portscourt import settings
# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')

class MainManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['name']) < 1:
            errors["name"] = "Name should not be blank." 
        if len(postData['username']) < 1:
            errors["username"] = "Username should not be blank."
        if len(postData['pw']) < 8:
            errors["pw_short"] = "Password is must be at least 8 characters."
        if postData['pw'] != postData['pw_confirm']:
            errors["pw_diff"] = "Passwords don't match."
        if len(postData['email']) < 1 or not EMAIL_REGEX.match(postData['email']):
            errors["email_invalid"] = "Please enter valid email."
        if User.objects.filter(email=postData["email"]):
            errors["email_exists"] = "Email already exists."        
        if User.objects.filter(username = postData["username"]):
            errors["username_exists"] = "Username already exists."
        if len(postData['address']) <1:
            errors['address_issue'] = "Enter a valid address."
        if len(postData['zipcode']) != 5:
            errors["zipcode_issue"] = "Enter a valid zipcode."
        if len(postData['city']) < 1:
            errors["city_missing"] = "City should not be blank."
        if len(postData['state']) < 1:
            errors["state_missing"] = "State should not be blank."
        maps_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={},+{},+{}&key=AIzaSyCgUgWi-8U3WvIONYaymBWSv59MKD-M_Ik'.format(postData['address'].replace(" ","+"), postData['city'].replace(" ", "+"), postData['state'])
        print maps_url
        req = requests.get(maps_url)
        # print req
        real_address = json.loads(req.content.decode('utf-8'))
        # print real_address['results'][0]['partial_match']
        if 'partial_match' in real_address['results'][0]:
            errors["notrealAddress"] = "Address is not valid."
        if len(postData['bday']) == 0:
            errors["no_bday"] = "Enter a valid date."
        else:
            today = datetime.today()
            eighteen = today + timedelta(days=6570)
            my_bday = datetime.strptime(postData['bday'], "%Y-%m-%d")
            if my_bday > eighteen:
                errors["too_young"] = "You must be at least 18 years of age to join."
        return errors 
    def login_validator(self, postData):
        errors = {}
        try:
            User.objects.get(username=postData['username'])
            if not bcrypt.checkpw(postData['pw'].encode(), User.objects.get(username=postData['username']).password.encode()):
                errors["issue_1"] = "Username or password is invalid."
        except User.DoesNotExist:
            errors["issue_2"] = "Username or password is invalid."
        return errors

    def edit_validator(self, postData, session):
        errors = {}
        if len(postData['name']) < 1:
            errors["name"] = "Name shouldn't be blank." 
        if len(postData['username']) < 1:
            errors["username"] = "Username shouldn't be blank."
        if len(postData['email']) < 1 or not EMAIL_REGEX.match(postData['email']):
            errors["email_invalid"] = "Please enter valid email."
        if len(postData['zipcode']) != 5:
            errors["zipcode_issue"] = "Enter a valid zipcode."
        if len(postData['city']) < 1:
            errors["city_missing"] = "City should not be blank."
        if len(postData['state']) < 1:
            errors["state_missing"] = "State should not be blank."
        maps_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={},+{},+{}&key=AIzaSyCgUgWi-8U3WvIONYaymBWSv59MKD-M_Ik'.format(postData['address'].replace(" ","+"), postData['city'].replace(" ", "+"), postData['state'])
        print maps_url
        req = requests.get(maps_url)
        # print req
        real_address = json.loads(req.content.decode('utf-8'))
        # print real_address['results'][0]['partial_match']
        if 'partial_match' in real_address['results'][0]:
            errors["notrealAddress"] = "Address is not valid."
        original_email = User.objects.get(email=postData['email']).email
        if postData['email'] != original_email and len(User.objects.filter(email=postData["email"])) > 1:
            errors["email_exists"] = "Email already exists."        
        if User.objects.filter(Q(username = postData["username"]) & ~Q(id=session['id'])):
            errors["username_exists"] = "Username already exists."
        if len(postData['bday']) == 0:
            errors["no_bday"] = "Enter a valid date."
        else:
            today = datetime.today()
            eighteen = today + timedelta(days=6570)
            my_bday = datetime.strptime(postData['bday'], "%Y-%m-%d")
            if my_bday > eighteen:
                errors["too_young"] = "You must be at least 18 years of age to join."
        return errors 

    def edit_pw_validator(self, postData, session):
        errors = {}
        if not bcrypt.checkpw(postData['pw'].encode(), User.objects.get(id=session['id']).password.encode()):
            errors["issue_1"] = "Password is invalid."
        if len(postData['new_pw']) < 8:
            errors["new_pw_short"] = "Password is too short."
        if postData['new_pw'] != postData['new_pw_confirm']:
            errors["new_pw_diff"] = "Passwords don't match."
        return errors

    def photo_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors["title_length"] = "Title needs to be longer."
        return errors
    
    def group_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors["group_name_length"] = "Group name needs to be longer."
        if len(postData['description']) < 3:
            errors["group_description"] = "Group description needs to be longer."
        if Group.objects.filter(name=postData['name']):
            errors["group_name_exists"] = "Group already exists."
        return errors

    def plan_validator(self, postData):
        errors = {}
        if len(postData['name']) < 1:
            errors["name"] = "Name should not be blank." 
        if len(postData['description']) < 1:
            errors["description"] = "Description should not be blank."
        if len(postData['zipcode']) != 5:
            errors["zipcode_issue"] = "Enter a valid zipcode."
        if len(postData['city']) < 1:
            errors["city_missing"] = "City should not be blank."
        if len(postData['state']) < 1:
            errors["state_missing"] = "State should not be blank."
        maps_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={},+{},+{}&key=AIzaSyCgUgWi-8U3WvIONYaymBWSv59MKD-M_Ik'.format(postData['address'].replace(" ","+"), postData['city'].replace(" ", "+"), postData['state'])
        print maps_url
        req = requests.get(maps_url)
        # print req
        real_address = json.loads(req.content.decode('utf-8'))
        # print real_address['results'][0]['partial_match']
        if 'partial_match' in real_address['results'][0]:
            errors["notrealAddress"] = "Address is not valid."
        if len(postData['date']) == 0:
            errors["no_date"] = "Enter a valid date."
        else:
            today = datetime.today()
            date = datetime.strptime(postData['date'].replace("T"," "), "%Y-%m-%d %H:%M")
            if today > date:
                errors["in_future"] = "Plan must be a future date."
        return errors 

def user_directory_path(instance, filename):
    return '{0}user_{1}/{2}_{3}'.format(settings.MEDIA_URL,instance.uploader.id, filename, uuid.uuid4())
def user_directory_path_profile(instance, filename):
    return '{0}user_{1}/{2}_{3}'.format(settings.MEDIA_URL, instance.id, filename, uuid.uuid4())

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthday = models.DateField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zipcode = models.IntegerField()
    user_level = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    profile_pic = models.ImageField()
    
    objects = MainManager()
    
class Photo(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length = 255, null=True)
    description = models.TextField(max_length = 500, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    uploader = models.ForeignKey(User, related_name='uploaded_photos')
    likers = models.ManyToManyField(User, related_name='liked_photos')
    objects = MainManager()

class Tag(models.Model):
    content = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    tagged_photo = models.ManyToManyField(Photo, related_name="tags")

    objects = MainManager()

class Comment(models.Model):
    review = models.IntegerField()
    content = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    writer = models.ForeignKey(User, related_name='my_comments')
    photo_commented = models.ForeignKey(Photo, related_name='comments', null=True)

    objects = MainManager()

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    tags = models.TextField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    creator = models.ForeignKey(User, related_name="created_groups")
    members = models.ManyToManyField(User, related_name='my_groups')

    objects = MainManager()

class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    date = models.DateTimeField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zipcode = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    members = models.ManyToManyField(User, related_name='joined_plans')
    host = models.ForeignKey(User, related_name="my_plans")

    objects = MainManager()

class Chat(models.Model):
    messengers = models.ManyToManyField(User, related_name="my_chatrooms", null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    
class Message(models.Model):
    message = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, related_name="my_messages")
    chatroom = models.ForeignKey(Chat, related_name="chats_messages")
