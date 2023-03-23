from django.shortcuts import render,redirect,get_object_or_404
from .forms import LibLoginForm,SellBookForm,AddBookForm,LibRegisterForm
from django.contrib import messages
from .models import Library,Books
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from datetime import datetime,timedelta,date
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    if request.session.has_key('lib_name'):
        lib_name = request.session['lib_name']
        return render(request,"index.html",{'lib_name':lib_name})
    return render(request,"index.html")

def library_usage(request):
    return render(request,"lib_info.html")

def visitor_usage(request):
    return render(request,"visitor_info.html")

def lib_login(request):
    form = LibLoginForm()
    if request.method == "POST":
        form = LibLoginForm(request.POST)
        if form.is_valid():
            lib_name = form.cleaned_data.get("lib_name")
            lib_password = form.cleaned_data.get("lib_password")
            lib = Library.objects.filter(lib_name=lib_name)
            if lib:
                lib = Library.objects.get(lib_name=lib_name)
                if lib_password != lib.lib_password:
                    messages.warning(request,"Library Password Is Wrong")
                    return redirect("library:lib_login")
                else:
                    username = form.cleaned_data.get("username")
                    password = form.cleaned_data.get("password")
                    
                    user = authenticate(username=username,password=password)
                    context = {
                        'form':form
                    }
                    if user is None:
                        form = LibLoginForm()
                        context = {
                            'form':form
                        }
                        messages.warning(request,"Username or Password is Wrong")
                        return render(request,"login.html",context)
                    request.session['lib_name'] = lib_name
                    lib_id = lib.id
                    request.session['lib_id'] = lib_id
                    request.session['lib_city'] = lib.lib_city
                    messages.success(request,"You Have Been Successfully Logged In")
                    auth_login(request,user)
                    return redirect("index")
            else:
               messages.warning(request,"Library Could Not Found") 
               return redirect("library:lib_login")
            
    return render(request,"login.html",{"form":form})

def lib_register(request):
    form = LibRegisterForm()
    if request.method == "POST":
        form = LibRegisterForm(request.POST)
        if form.is_valid():
            lib_name = form.cleaned_data.get("lib_name")
            lib = Library.objects.filter(lib_name=lib_name)
            if lib:
                lib = Library.objects.get(lib_name=lib_name)
                lib_password = form.cleaned_data.get('lib_password')
                if lib_password != lib.lib_password:
                    messages.warning(request,"Library Password Is Wrong")
                    return redirect("library:lib_register")
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                newUser = User(username = username)
                newUser.set_password(password)
                
                newUser.save()
                auth_login(request,newUser)
                request.session['lib_name'] = lib_name
                request.session['lib_city'] = lib.lib_city
                messages.success(request,"You Have Been Registered Successfully")
                return redirect("index")
            else:
                messages.warning(request,"Library Could Not Found")
                return redirect("library:lib_register")
    return render(request,"register.html",{'form':form})
@login_required(login_url="/library/lib_login")
def dashboard(request):
    key_author = request.GET.get("key_author")
    key_book = request.GET.get("key_book")
    if key_author:
        books = Books.objects.filter(book_author__contains=key_author,lib_name=request.session['lib_name'])
        return render(request,"dashboard.html",{'books':books})
    elif key_book:
        books = Books.objects.filter(book_name__contains=key_book,lib_name=request.session['lib_name'])
        return render(request,"dashboard.html",{'books':books})
    elif key_author and key_book:
        books = Books.objects.filter(book_name__contains=key_book,book_author__contains=key_author,lib_name=request.session['lib_name'])
        return render(request,"dashboard.html",{'books':books})
    books = Books.objects.filter(lib_name=request.session['lib_name'])
    return render(request,"dashboard.html",{'books':books})
@login_required(login_url="/library/lib_login")
def lib_logout(request):
    logout(request)
    request.session.clear()
    messages.success(request,"You Have Been Logged Out Successfully")
    return redirect("index")

def visitor(request):
    key_lib = request.GET.get("key_lib")
    key_city = request.GET.get("key_city")
    if key_lib: 
        libraries = Library.objects.filter(lib_name__contains=key_lib)
    elif key_city:
        Library.objects.filter(lib_city__contains=key_city)
    elif key_city and key_lib:
        Library.objects.filter(lib_name__contains=key_lib,lib_city__contains=key_city)
    libraries = Library.objects.all()
    return render(request,"visitor.html",{'libraries':libraries})
@login_required(login_url="/library/lib_login")
def sellbook(request,id):
    book = get_object_or_404(Books,id = id)
    form = SellBookForm(request.POST or None)
    if form.is_valid():
        buyer_name = form.cleaned_data.get('buyer_name')
        buyer_phone = form.cleaned_data.get('buyer_phone')
        buyer_email = form.cleaned_data.get('buyer_email')
        book.buyer_name = buyer_name
        book.buyer_phone = buyer_phone
        book.buyer_email = buyer_email
        todaydate = date.today()
        receivedate = todaydate + timedelta(days=60)
        book.buying_date = todaydate
        book.receive_date = receivedate
        book.avaible = False
        book.save()
        messages.success(request,"Book Has Been Sold")
        return redirect("library:dashboard")
    return render(request,"sell.html",{'form':form,'book':book})
@login_required(login_url="/library/lib_login")
def receivebook(request,id):
    book = get_object_or_404(Books,id = id)
    if request.method == "POST":
        book.avaible = True
        book.buyer_name = None
        book.buyer_phone = None
        book.buyer_email = None
        book.buying_date = None
        book.receive_date = None
        book.save()
        messages.success(request,"You Have Been Received Book")
        return redirect("library:dashboard")
    return render(request,"receive.html",{'book':book})
@login_required(login_url="/library/lib_login")
def addbook(request):
    form = AddBookForm(request.POST or None)
    if form.is_valid():
        book_name = form.cleaned_data.get('book_name')
        book_author = form.cleaned_data.get('book_author')
        newbook = Books(book_name = book_name,book_author = book_author)
        newbook.lib_name = request.session['lib_name']
        newbook.lib_city = request.session['lib_city']
        newbook.avaible = True
        newbook.buyer_name = None
        newbook.buyer_phone = None
        newbook.buyer_email = None
        newbook.buying_date = None
        newbook.receive_date = None
        newbook.save()
        messages.success(request,"Book Has Been Added Successfully..")
        return redirect("library:dashboard")
    return render(request,"addbook.html",{'form':form})
@login_required(login_url="/library/lib_login")
def deletebook(request,id):
    book = get_object_or_404(Books,id = id)
    if request.method == "POST":
        book.delete()
        messages.success(request,"Book Has Been Deleted Successfully")
        return redirect("library:dashboard")
    return render(request,"delete.html")
@login_required(login_url="/library/lib_login")
def detailbook(request,id):
    book = get_object_or_404(Books,id = id)
    return render(request,"detail.html",{'book':book})

def library(request,id):
    library = get_object_or_404(Library,id=id)
    key_book = request.GET.get("key_book")
    key_author = request.GET.get("key_author")
    if key_book:
        books = Books.objects.filter(book_name__contains=key_book,lib_name=library.lib_name)
        return render(request,"library.html",{"library":library,"books":books})
    elif key_author:
        books = Books.objects.filter(book_author__contains=key_author,lib_name=library.lib_name)
        return render(request,"library.html",{"library":library,"books":books})
    elif key_book and key_author:
        books = Books.objects.filter(book_name__contains=key_book,book_author__contains=key_author,lib_name=library.lib_name)
        return render(request,"library.html",{"library":library,"books":books})
    books = Books.objects.filter(lib_name=library.lib_name)
    return render(request,"library.html",{"library":library,"books":books})
