from ast import Return
from asyncio.windows_events import NULL
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
import datetime
from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users,admin_only
from django.contrib.auth.models import Group
from datetime import datetime

#the main app for the librarian to access the system
@login_required(login_url='login')
@admin_only
def issuereturn(request): 
    form = SearchField()
    issueform = IssueForm()
    returnform = ReturnForm()
    if request.method == "GET":
        if request.GET.get('searchinput'):
            form = SearchField(request.GET)
            if form.is_valid():
                #populating()
                # print("Populated")
                query = form.cleaned_data.get('searchinput')
                start = Title()
                try:

                        vector = SearchVector('title', weight = 'B', config = 'english') + SearchVector('author', weight = 'A', config = 'english')
                        mango = Title.objects.annotate(search = vector).filter(search = SearchQuery(query))
                
                        if mango:
                            c = mango.count()
                            return render(request, "issuereturn.html", {'form': form, 'bookdata' : mango, 'count' : c, 'result' : "searchvector", 'issueform' : issueform, 'returnform' : returnform})

                        else:
                            apple = Title.objects.annotate(similarity=TrigramSimilarity('author', query) + TrigramSimilarity('title', query),).filter(similarity__gt=0.12) .order_by('-similarity')
                            c = apple.count()
                            return render(request, "issuereturn.html", {'form': form, 'bookdata' : apple, 'count' : c, 'result' : "trigram", 'issueform' : issueform, 'returnform' : returnform})
                except:
                    return render(request, "issuereturn.html", {'form': form, 'issueform' : issueform, 'returnform' : returnform})


        if request.GET.get('issue_registration_no'):
            issueform = IssueForm(request.GET)
            if issueform.is_valid():
                student_reg_no = issueform.cleaned_data.get('issue_registration_no')
                title = request.GET.get('modal_title')
                author = request.GET.get('modal_author')

                try:
                    student = StudentProfile.objects.get(registration_no = student_reg_no) 
                except:
                    print("no registration")
                    return render(request, "issuereturn.html", {'form': form, 'issueform' : issueform, 'returnform' : returnform})

                acc_no = issueform.cleaned_data.get('acc_no')

                try:
                    book = Books.objects.get(acc_no = acc_no)
                    print(book.uid.author)
                except:
                    print("no accession")
                    return render(request, "issuereturn.html", {'form': form, 'issueform' : issueform, 'returnform' : returnform})


                if book.student_id != "":
                    print("kaa hua pehle to diyen hain")
                    return render(request, "issuereturn.html", {'form': form, 'issueform' : issueform, 'returnform' : returnform})


                if title != book.uid.title or author != book.uid.author:
                    print("bhul bhaal book aithor")
                    return render(request, "issuereturn.html", {'form': form, 'issueform' : issueform, 'returnform' : returnform})

                doi = date.today()
                edor = date.today() + timedelta(days=15)
                issue_mode = "15 Days"
                log = Log(registration_no=student_reg_no, acc_no=acc_no, edor=edor, issue_mode="15 Days")
                log.save()
                print("All successfull")
                books = Books.objects.get(acc_no = acc_no)
                if books:
                    title = Title.objects.get(uid = books.uid.uid)
                    title.total_book_count = title.total_book_count - 1
                    title.save()

                    books.student_id = student_reg_no
                    books.save()
                    
            return render(request, "issuereturn.html", {'form': form, 'issueform' : issueform, 'returnform' : returnform})

        if request.GET.get('return_acc_no'):
            returnform = ReturnForm(request.GET)
            if returnform.is_valid():
                acc_no = returnform.cleaned_data.get('return_acc_no')
                title = request.GET.get('modal_r_title')
                author = request.GET.get('modal_r_author')

                try:
                    book = Books.objects.get(acc_no = acc_no)
                except:
                    return render(request, "issuereturn.html", {'form': form, 'issueform' : issueform, 'returnform' : returnform})

                try:
                    title = Title.objects.get(uid = book.uid.uid)
                except:
                    return render(request, "issuereturn.html", {'form': form, 'issueform' : issueform, 'returnform' : returnform})

                if title != book.uid.title or author != book.uid.author:
                    return render(request, "issuereturn.html", {'form': form, 'issueform' : issueform, 'returnform' : returnform})
                
                registration_no = book.student_id
                book.student_id = ""
                book.save()

                title.total_book_count = title.total_book_count + 1
                title.save()

                log = Log.objects.filter(acc_no = acc_no, registration_no = registration_no)[0]
                print(log)
                log.dor = date.today()
                log.save()  

            return render(request, "issuereturn.html", {'form': form, 'issueform' : issueform, 'returnform' : returnform})

        else:
            return render(request, "issuereturn.html", {'form': form, 'issueform' : issueform, 'returnform' : returnform})

    return render(request, "issuereturn.html", {'form': form, 'issueform' : issueform, 'returnform' : returnform})




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
def register(request):
    form = CreateUserForm()
    profile_form = StudentProfileForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)
        profile_form = StudentProfileForm(request.POST)
        print(profile_form)
        print("HelloRegister")
        print(profile_form.is_valid())
        if form.is_valid() or profile_form.is_valid() :

            user = form.save()
            print(user)
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            group = Group.objects.get(name='student')
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            print(form.cleaned_data.get('username'))
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
        else:
            messages.error(request,"Error")


    return render(request, 'register.html', {'form': form, 'profile_form': profile_form})




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
    print(request.user.id)
    ll = []
    fine=[]
    collect_list=[]
    b_author = []
    edor=[]
    if request.user.is_authenticated:
        print(request.user.username)
        student_profile = StudentProfile.objects.get(user = request.user.id)
        book = Books.objects.filter(student_id = student_profile.registration_no)
        curDT = datetime.now()
        curDTSTR=curDT.strftime("%m/%d/%Y")
        print(curDTSTR)

        for i in book:
            print(i.acc_no)
            print(i.student_id)
            log = Log.objects.filter(acc_no = i.acc_no, registration_no = i.student_id, dor = None)
            book = Books.objects.filter(acc_no = log[0].acc_no)
            print(log[0].edor)
            date_time = log[0].edor.strftime("%m/%d/%Y")
            #print(date_time)
            print((datetime.strptime(curDTSTR, "%m/%d/%Y")-datetime.strptime(date_time, "%m/%d/%Y")).days)
            ll.append(book[0].uid.title)
            b_author.append(book[0].uid.author)
            edor.append(log[0].edor)
            total_fine=(datetime.strptime(curDTSTR, "%m/%d/%Y")-datetime.strptime(date_time, "%m/%d/%Y")).days*5
            if total_fine < 0:
                total_fine=0
            fine.append(total_fine)
        collect_list=zip(ll,b_author,edor,fine)
        #student details
        sname=request.user.first_name+" " +request.user.last_name
        sdept=student_profile.dept
        sphone_number=student_profile.phone_number
        sregistration_no=student_profile.registration_no
        saddress=student_profile.address
        smail=request.user.email;
        total_count = len(ll)
        print("list count")
        print(ll)

    return render(request,'student.html', {"list":ll,"fine":fine,"collect_list":collect_list, "total_count":total_count,"name":sname,"dept":sdept,"sphonenumber":sphone_number,"registration_no":sregistration_no,"address":saddress, "smail" : smail})


@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def teacher(request):
    return render(request, 'teacher.html')



@login_required(login_url='login')
@admin_only
def addbook(request):
    title_form = AddTitleForm()

    # uid = Title.objects.latest('uid')
    # print(uid.uid)
    # acc_no = Books.objects.latest('acc_no')
    # print(acc_no.acc_no)

    if request.method == 'POST':
        title_form = AddTitleForm(request.POST)
        if title_form.is_valid():
            #Getting form data and storing it into the title table
            title = title_form.cleaned_data['title']
            author = title_form.cleaned_data['author']
            total_book_count = title_form.cleaned_data['total_book_count']
            title_object = Title.objects.latest('uid')
            uid = title_object.uid + 1
            title_model = Title(uid, title, author, total_book_count)
            title_model.save()

            #Adding books in books table in loop
            books_object = Books.objects.latest('acc_no')
            acc_no = books_object.acc_no + 1;
            e_acc_no = acc_no + total_book_count
          

            for i in range(acc_no, e_acc_no):
                book_model = Books(title_model.uid, i, "", date.today())
                book_model.save()

        else:
            messages.error(request,"Error")
            print(title_form.errors)

    

    return render(request, "addbook.html", {'title_form' : title_form})