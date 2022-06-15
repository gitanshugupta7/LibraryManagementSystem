from django.contrib import admin
from django.urls import path, include
from Books_Title import views

urlpatterns = [
    path('', views.issuereturn, name="issuereturn"),
    path('login/',views.loginUser,name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('student/', views.student, name="student"),
    path('teacher/', views.teacher, name="teacher"),
    path('register/', views.register, name="register"),
    path('teacher_register/', views.teacher_register, name="teacher_register"),
    path('addbook', views.addbook, name="addbook"),
]