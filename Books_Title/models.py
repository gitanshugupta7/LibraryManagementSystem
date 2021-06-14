from django.db import models
import datetime
import uuid
from django.contrib.auth.models import User

# This table only saved the distinct titles in the library
class Title(models.Model):

    uid = models.IntegerField(default = 0, primary_key = True)
    title = models.CharField(default = "", max_length = 500)
    author = models.CharField(default = "", max_length = 100)
    total_book_count = models.IntegerField(default = 0)

    def __str__(self):
        return self.title

# This table stores all the copies available in the library and is connected to the titles table via foreign key
class Books(models.Model):

    uid = models.ForeignKey(Title, on_delete = models.CASCADE)
    acc_no = models.IntegerField(default = 0, primary_key = True)
    student_id = models.CharField(default = "", max_length = 20)
    last_used = models.DateField(auto_now_add = True, blank = True)

    def __str__(self):
        return str(self.acc_no)

# This is used to store student data in the system and is connected to django auth via onetoone field
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dept = models.CharField(max_length = 11, blank = False)
    phone_number = models.CharField(max_length = 11, blank = False)
    registration_no = models.CharField(max_length = 11, blank = False, primary_key = True)
    address = models.CharField(max_length = 50, default = "")
    unique_id = models.CharField(max_length = 11, blank = False)

    def __str__(self):
        return str(self.user)


# This is used to store teacher data in the system and is connected to django via onetoone field
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dept = models.CharField(max_length = 11, blank=False)
    phone_number = models.CharField(max_length = 11, blank = False)
    address = models.CharField(max_length = 50, default = "")
    unique_id = models.CharField(max_length = 11, blank = False)

    def __str__(self):
        return str(self.user)


# This is an important table, the librarians pre register the students into the system and only selected
# students or teachers can register and login into the system
class ID(models.Model):
   unique_id = models.CharField(max_length = 8)
   email = models.EmailField()
   unique_id = models.CharField(max_length = 11, blank = False)

   
 



