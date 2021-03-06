from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from calendar import monthrange
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.forms import inlineformset_factory
from datetime import timedelta as tdelta
from django.utils import timezone
import datetime
from datetime import date, timedelta, datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import _datetime
from .models import *
from django.contrib.auth.models import Group, User

class SearchField(forms.Form):
    searchinput = forms.CharField(max_length = 100, label = "Search Book", widget=forms.TextInput(attrs={'placeholder': 'Search here'}))

    class Meta:
        fields = ["searchinput",]



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class StudentProfileForm(forms.ModelForm):
    
    class Meta:
        model = StudentProfile
        fields = ['dept','phone_number','registration_no','address']


class TeacherProfileForm(forms.ModelForm):
    
    class Meta:
        model = TeacherProfile
        fields = '__all__'


class IssueForm(forms.Form):
    issue_registration_no = forms.CharField(max_length=11, label="Enter Student Registration Number", widget=forms.TextInput(attrs={'placeholder': 'Enter Student Registration No.'}))
    acc_no = forms.IntegerField(label="Enter The Accession Number", widget=forms.NumberInput(attrs={'placeholder': 'Enter Accession No.'}))

    class Meta:
        fields = ["issue_registration_no", "acc_no"] 


class ReturnForm(forms.Form):
    return_acc_no = forms.IntegerField(label="Enter The Accession Number", widget=forms.NumberInput(attrs={'placeholder': 'Enter Accession No.'}))

    class Meta:
        fields = ["return_acc_no"] 


class AddTitleForm(forms.Form):
    title = forms.CharField(max_length=100, label="Enter Title", widget=forms.TextInput(attrs={'placeholder': 'Enter Title.'}))
    author = forms.CharField(max_length=11, label="Enter Author", widget=forms.TextInput(attrs={'placeholder': 'Enter Author.'}))
    total_book_count = forms.IntegerField(label="Enter Book Count", widget=forms.NumberInput(attrs={'placeholder': 'Enter Number of Copies'}))
    
    class Meta:
        fields = ['title', 'author', 'total_book_count']

class AddBookCopies(forms.Form):
    no_of_copies = forms.IntegerField(label="Enter No Of Copies", widget=forms.NumberInput(attrs={'placeholder': 'Enter Number of Copies'}))
    
    class Meta:
        fields = ['no_of_copies']
