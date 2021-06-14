from django.contrib.postgres.search import *
from django.contrib.postgres.operations import  *
from .models import *
from .forms import *
from .populatedata import *
from . import views
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from calendar import monthrange
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from datetime import timedelta as tdelta
from django.utils import timezone
from datetime import date, timedelta, datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import _datetime
from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users,admin_only
from django.contrib.auth.models import Group


#the main app for the librarian to access the system
@login_required(login_url='login')
@admin_only
def issuereturn(request): 
    form = SearchField()
    if request.method == "GET":
        form = SearchField(request.GET)
        if form.is_valid():
            # populating()
            # print("Populated")
            query = form.cleaned_data.get('searchinput')
            start = Title()

            vector = SearchVector('title', weight = 'B', config = 'english') + SearchVector('author', weight = 'A', config = 'english')
            mango = Title.objects.annotate(search = vector).filter(search = SearchQuery(query))
            
            if mango:
                
                c = mango.count()
                return render(request, "issuereturn.html", {'form': form, 'bookdata' : mango, 'count' : c, 'result' : "searchvector"})
                
            else:
                apple = Title.objects.annotate(similarity=TrigramSimilarity('author', query) + TrigramSimilarity('title', query),).filter(similarity__gt=0.12) .order_by('-similarity')
                c = apple.count()
                return render(request, "issuereturn.html", {'form': form, 'bookdata' : apple, 'count' : c, 'result' : "trigram"})


    return render(request, "issuereturn.html", {'form': form})




#login page will be rendered by this function
@unauthenticated_user
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('issuereturn')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'login.html', context)


#this is to logout from the system
def logoutUser(request):
    logout(request)
    return redirect('login')



#registration function for students only
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    profile_form = StudentProfileForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)
        profile_form = StudentProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():

            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            group = Group.objects.get(name='student')
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    return render(request, 'register.html',{'form':form,'profile_form':profile_form})




#registration function for teachers only
@unauthenticated_user
def teacher_register(request):
    form = CreateUserForm()
    profile_form=TeacherProfileForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        profile_form = TeacherProfileForm(request.POST)
        #profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            group = Group.objects.get(name='teacher')
            user.groups.add(group)

            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    return render(request, 'teacher_register.html',{'form':form,'profile_form':profile_form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def student(request):
    return render(request,'student.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def teacher(request):
    return render(request, 'teacher.html')



