# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from models import *
import bcrypt

# Create your views here.
def index(request):
    if 'id' in request.session:
        redirect('/main')
    return render(request, 'ports/index.html')

def start(request):
    if 'id' in request.session:
        redirect('/main')
    return render(request, 'ports/start.html')

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
        curr = User.objects.create(name=request.POST['name'], username=request.POST['username'], email=request.POST['email'], password=hp, birthday=my_bday, user_level=my_position, zipcode=request.POST['zipcode'],city=request.POST['city'], state=request.POST['state'])
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
    context = {
        'user' : User.objects.get(id=request.session['id']),
        'photographers': User.objects.filter(Q(user_level=1) & ~Q(id=request.session['id'])),
        'models': User.objects.filter(Q(user_level=2) & ~Q(id=request.session['id'])),
        'clients': User.objects.filter(Q(user_level=3) & ~Q(id=request.session['id'])),
        'plans': Plan.objects.exclude(host_id=request.session['id']),
        'my_plans': Plan.objects.filter(host_id=request.session['id']),
        'today': datetime.now(),
        'groups':Group.objects.exclude(members__id=request.session['id']),
        'my_groups': Group.objects.filter(members__id=request.session['id'])
    }
    return render(request, 'ports/main.html', context)

def edit_user(request):
    if not 'id' in request.session:
        return redirect('/')
    context = {
        'user' : User.objects.get(id=request.session['id']),
    }
    return render(request, 'ports/edit_user.html', context)

def edit_user_process(request):
    if request.method !="POST":
        return redirect('/edit_user')
    errors = User.objects.edit_validator(request.POST, request.session)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/edit_user')
    a = User.objects.get(id=request.session['id'])
    a.name = request.POST['name']
    a.email = request.POST['email']
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
        return redirect('/edit_user')
    a = User.objects.get(id=request.session['id'])
    hp = bcrypt.hashpw(request.POST['new_pw'].encode(), bcrypt.gensalt())
    a.password = hp
    a.save()
    return redirect('/main')

def edit_profile_pic_process(request):
    if request.method !="POST":
        return redirect('/edit_user')
    a = User.objects.get(id=request.session['id'])
    print request.FILES
    if 'prof_pic' in request.FILES:
        a.profile_pic = request.FILES['prof_pic']
        a.save()
    else:
        messages.error(request, "No Photo Uploaded!")
        return redirect('/edit_user')
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
    context={
        'my_plans_exclude': Plan.objects.filter(host_id=request.session['id']).exclude(members__id=user.id),
        'my_plans_include': Plan.objects.filter(Q(host_id=request.session['id']) & Q(members__id=user.id)),
        'user': user,
        'portfolio': User.objects.get(id=id).uploaded_photos.all()[:2],
    }
    return render(request, 'ports/users.html', context)

def add_photo_process(request, id):
    if request.method !="POST":
        return redirect('/main')
    errors = User.objects.photo_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/edit_user')  
    a = Photo.objects.create(image=request.FILES['portfolio_pic'], title=request.POST['title'],uploader=User.objects.get(id=id))
    user_id = User.objects.get(id=id).id
    return redirect('/portfolio/{}'.format(id))

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
    return redirect('/main')

def show_plan(request, id):
    if not 'id' in request.session:
        return redirect('/')
    context = {
        'user' : User.objects.get(id=request.session['id']),
        'plan' : Plan.objects.get(id=id),
    }
    return render(request, 'ports/show_plan.html', context)
    
def edit_plan_process(request, id):
    if request.method !="POST":
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

def new_group(request):
    if request.method !="POST":
        return redirect('/main')
    me = User.objects.get(id=request.session['id'])
    this_group = Group.objects.create(name=request.POST['name'], description=request.POST['description'], tags=request.POST['tag'], creator = me)
    this_group.members.add(me)
    this_group.save()
    return redirect('/groups/'+this_group.id)

def show_group(request, id):
    if not 'id' in request.session:
        return redirect('/')
    context={
        group: Group.objects.get(id=id),
    }
    return render(request, 'ports/show_group.html', context)

def edit_group_process(request,id):
    if request.method !="POST":
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
    if this_group.members_set.filter(id=me.id).exists():
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

def log_out(request):
    if 'id' in request.session:
        request.session.clear()
    return redirect('/')