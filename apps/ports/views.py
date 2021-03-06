# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from models import *
import bcrypt
from portscourt import settings

allStates=["AL", "AK", "AR", "AZ", "CA","CO","CT","DE","FL","GA","HI","IA","ID","IL","IN","KS","KY","LA","MA","ME","MD","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VA","VT","WA","WI","WV","WY"]
# Create your views here.
def index(request):
    print("In the index method")
    if 'id' in request.session:
        redirect('/main')
    return render(request, 'ports/index.html')

def start(request):
    if 'id' in request.session:
        redirect('/main')
    context={
        'all_states': allStates,
    }
    return render(request, 'ports/start.html',context)

def process(request, action):
    if request.method !="POST":
        return redirect('/')
    if action == 'reg':
        errors = User.objects.register_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/start')
        # encrypting passwords
        hp = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
        my_bday = datetime.strptime(request.POST['bday'], "%Y-%m-%d")
        # access level
        try:
            User.objects.get(id=1)
            my_position = int(request.POST['position'])
        except User.DoesNotExist:
            my_position = 9
        curr = User.objects.create(name=request.POST['name'], username=request.POST['username'], email=request.POST['email'], password=hp, birthday=my_bday, user_level=my_position, address=request.POST['address'], zipcode=request.POST['zipcode'],city=request.POST['city'], state=request.POST['state'])
        request.session['id'] = curr.id
    else:
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/start')
        request.session['id'] = User.objects.get(username=request.POST['username']).id
    return redirect('/main')

def main(request):
    if not 'id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    context = {
        'user' : user,
        'photographers': User.objects.filter(Q(user_level=1) & ~Q(id=request.session['id'])),
        'models': User.objects.filter(Q(user_level=2) & ~Q(id=request.session['id'])),
        'clients': User.objects.filter(Q(user_level=3) & ~Q(id=request.session['id'])),
        'plans': Plan.objects.exclude(host_id=request.session['id']),
        'my_plans': Plan.objects.filter(host_id=request.session['id']),
        'today': datetime.now(),
        'groups':Group.objects.exclude(members__id=request.session['id']),
        'my_groups': Group.objects.filter(members__id=request.session['id']),
        'all_states': allStates,
        'users': User.objects.exclude(id=request.session['id']),
    }
    print('Got to right before render')
    return render(request, 'ports/main.html', context)

def edit_user_process(request):
    if request.method !="POST":
        return redirect('/users/{}'.format(request.session['id']))
    errors = User.objects.edit_validator(request.POST, request.session)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/users/{}'.format(request.session['id']))
    a = User.objects.get(id=request.session['id'])
    a.name = request.POST['name']
    a.email = request.POST['email']
    a.address = request.POST['address']
    a.city = request.POST['city']
    a.zipcode =request.POST['zipcode']
    a.state = request.POST['state']
    a.user_level = request.POST['position']
    a.birthday = datetime.strptime(request.POST['bday'], "%Y-%m-%d").date()
    a.save()
    return redirect('/main')

def edit_pw_process(request):
    if request.method !="POST":
        return redirect('/main')
    errors = User.objects.edit_pw_validator(request.POST, request.session)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/users/{}'.format(request.session['id']))
    a = User.objects.get(id=request.session['id'])
    hp = bcrypt.hashpw(request.POST['new_pw'].encode(), bcrypt.gensalt())
    a.password = hp
    a.save()
    return redirect('/main')

def edit_profile_pic_process(request):
    if request.method !="POST":
        return redirect('/users/{}'.format(request.session['id']))
    a = User.objects.get(id=request.session['id'])
    print request.FILES
    if 'prof_pic' in request.FILES:
        a.profile_pic = request.FILES['prof_pic']
        a.save()
    else:
        messages.error(request, "No Photo Uploaded!")
        return redirect('/users/{}'.format(request.session['id']))
    return redirect('/main')

def manage_users(request):
    a = User.objects.get(id=request.session['id'])
    if a.user_level != 9:
        return redirect('/main')
    context = {
        'users': User.objects.all().exclude(user_level=9),
    }
    return render(request, 'ports/manage_users.html', context)

def admin_edit(request, id):
    if not 'id' in request.session:
        return redirect('/')
    a = User.objects.get(id=request.session['id'])
    if a.user_level != 9:
        return redirect('/main')
    context = {
        'user': User.objects.all().get(id=id),
    }
    return render(request, 'ports/admin_edit.html', context)

def admin_edit_process(request, id):
    if request.method !="POST":
        return redirect('/main')
    context = {
        'user': User.objects.all().get(id=id),
    }
    return redirect('/manage_users')

def delete_user(request, id):
    if not 'id' in request.session:
        return redirect('/')
    a = User.objects.get(id=request.session['id'])
    if a.user_level != 9:
        return redirect('/main')
    b = User.objects.get(id=id)
    b.delete()
    return redirect('/manage_users')

def portfolio(request, id):
    if not 'id' in request.session:
        return redirect('/')
    user = User.objects.get(id=id)
    context= {
        'user': user,
        'images': Photo.objects.filter(uploader=user),
    }
    return render(request, 'ports/portfolio.html', context)

def users(request, id):
    if not 'id' in request.session:
        return redirect('/')
    user = User.objects.get(id=id)
    user_bday = user.birthday.strftime("%Y-%m-%d")
    me = User.objects.get(id=request.session['id'])
    if Chat.objects.filter(messengers__in=[user, me]).first() == None:
        new_chat = Chat.objects.create()
        new_chat.messengers.add(user, me)
        new_chat.save()
    chatroom = Chat.objects.filter(messengers__in=[user, me]).first()
    print chatroom.chats_messages.all()
    context={
        'my_plans_exclude': Plan.objects.filter(host_id=request.session['id']).exclude(members__id=user.id),
        'my_plans_include': Plan.objects.filter(Q(host_id=request.session['id']) & Q(members__id=user.id)),
        'user': user,
        'bday': user_bday,
        'logged_user': User.objects.get(id=request.session['id']),
        'portfolio': User.objects.get(id=id).uploaded_photos.all(), 
        'chatroom' : chatroom,
    }
    return render(request, 'ports/users.html', context)

def add_photo_process(request, id):
    if request.method !="POST":
        return redirect('/main')
    errors = User.objects.photo_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/users/{}'.format(id))  
    a = Photo.objects.create(image=request.FILES['portfolio_pic'], title=request.POST['title'],uploader=User.objects.get(id=id))
    user_id = User.objects.get(id=id).id
    return redirect('/users/{}'.format(id))

def add_profile_pic_process(request, id):
    if request.method !="POST":
        return redirect('/main')
    errors = User.objects.photo_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    if not a.profile_pic:
        Photo.objects.create(image=request.FILES['prof_pic'], title=request.POST['title'], uploader=a, user_profile=a)
    return redirect('/main')

def photo(request, id):
    if not 'id' in request.session:
        return redirect('/')
    photo = Photo.objects.get(id=id)
    context={
        'logged_user': User.objects.get(id=request.session['id']),
        'photo': photo,
    }
    return render(request, 'ports/photo.html', context)

def new_plan(request):
    if request.method !="POST":
        return redirect('/main')
    errors = Plan.objects.plan_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    a = User.objects.get(id=request.session['id'])
    dumb_date = request.POST['date'].replace("T"," ")
    new_date = datetime.strptime(dumb_date, "%Y-%m-%d %H:%M")
    b = Plan.objects.create(name=request.POST['name'], description=request.POST['description'], date = new_date, city=request.POST['city'], state=request.POST['state'], zipcode=request.POST['zipcode'], host=a)
    b.save()
    b.members.add(a)
    b.save()
    return redirect('/main')

def show_plan(request, id):
    if not 'id' in request.session:
        return redirect('/')
    this_plan = Plan.objects.get(id=id)
    plan_date = this_plan.date.strftime("%Y-%m-%d")
    context = {
        'logged_user' : User.objects.get(id=request.session['id']),
        'plan' : Plan.objects.get(id=id),
        'plan_date':plan_date,
    }
    return render(request, 'ports/show_plan.html', context)
    
def edit_plan_process(request, id):
    if request.method !="POST":
        return redirect('/plans/'+id)
    errors = Plan.objects.plan_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/plans/'+id)
    this_plan = Plan.objects.get(id=id)
    if request.session['id'] == this_plan.host.id:
        return redirect('/plans/'+id)
    this_plan.name = request.POST['name']
    this_plan.description = request.POST['decscription']
    dumb_date = request.POST['date'].replace("T"," ")
    new_date = datetime.strptime(dumb_date, "%Y-%m-%d %H:%M")
    this_plan.date = new_date
    this_plan.city = request.POST['city']
    this_plan.state = request.POST['state']
    this_plan.zipcode = request.POST['zipcode']
    return redirect('/plans/'+id)

def add_to_plan_process(request, id):
    if request.method !="POST":
        return redirect('/users/'+id)
    this_plan = Plan.objects.get(id=request.POST['add_plan'])
    new_person = User.objects.get(id=id)
    this_plan.members.add(new_person)
    this_plan.save()
    return redirect('/users/'+id)

def remove_from_plan_process(request, id):
    if request.method !="POST":
        return redirect('/users/'+id)
    this_plan = Plan.objects.get(id=request.POST['remove_plan'])
    new_person = User.objects.get(id=id)
    this_plan.members.remove(new_person)
    this_plan.save()
    return redirect('/users/'+id)

def delete_plan(request, id):
    this_plan= Plan.objects.get(id=id)
    if this_plan.host.id != request.session['id']:
        return redirect('/plans/'+id)
    this_plan.members.clear()
    this_plan.delete()
    return redirect('/main')


def new_group(request):
    if request.method !="POST":
        return redirect('/main')
    errors = Group.objects.group_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    me = User.objects.get(id=request.session['id'])
    this_group = Group.objects.create(name=request.POST['name'], description=request.POST['description'], creator = me)
    this_group.members.add(me)
    this_group.save()
    return redirect('/groups/'+str(this_group.id))

def show_group(request, id):
    if not 'id' in request.session:
        return redirect('/')
    context={
        'logged_user': User.objects.get(id=request.session['id']),
        'group': Group.objects.get(id=id),
    }
    return render(request, 'ports/show_group.html', context)

def edit_group_process(request,id):
    if request.method !="POST":
        return redirect('/groups/'+id)
    errors = Group.objects.group_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/groups/'+id)
    this_group=Group.objects.get(id=id)
    if request.session['id'] != this_group.creator.id:
        return redirect('/groups/'+id)
    this_group.name= request.POST['name']
    this_group.description=request.POST['description']
    this_group.tags=request.POST['tags']
    return redirect('/groups/'+id)

def join_group(request, id):
    this_group = Group.objects.get(id=id)
    me = User.objects.get(id=request.session['id'])
    if this_group.members.filter(id=me.id).exists():
        print ("already joined")
    else:
        this_group.members.add(me)
        this_group.save()
    return redirect('/groups/'+id)

def leave_group(request,id):
    this_group = Group.objects.get(id=id)
    me = User.objects.get(id=request.session['id'])
    this_group.members.remove(me)
    this_group.save()
    return redirect('/groups/'+id)

def remove_groupmember(request,group_id,user_id):
    this_group = Group.objects.get(id=group_id)
    if this_group.creator.id != request.session['id']:
        return redirect('/groups/'+group_id)
    this_user = User.objects.get(id=user_id)
    this_group.members.remove(this_user)
    this_group.save()
    return redirect('/groups/'+group_id)

def add_message(request, user_id):
    if request.method !="POST":
        return redirect('/users/'+user_id)
    me = User.objects.get(id=request.session['id'])
    other_user = User.objects.get(id=user_id)
    this_chatroom = Chat.objects.filter(messengers__in=[me, other_user]).first()
    print this_chatroom.chats_messages
    new_message = Message.objects.create(message=request.POST['message'], author=me, chatroom=this_chatroom)
    new_message.save()
    return redirect('/users/'+user_id)

def log_out(request):
    if 'id' in request.session:
        request.session.clear()
    return redirect('/')

def guest_login(request):
    request.session['id'] = User.objects.get(username='jeffreyahn').id
    return redirect('/main')