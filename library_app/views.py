from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import *
import matplotlib.pyplot as plt
from django.http import HttpResponse
from io import BytesIO
from collections import Counter
from .models import *
from .middlewares import *


# Create your views here.
def pie_chart_view(request):
    books = Book.objects.all()
    book_types = [book.type for book in books]
    type_count = dict(Counter(book_types))
    labels = type_count.keys()
    sizes = type_count.values()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})
    ax.axis('equal')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')


@auth
def home(request):
    books = Book.objects.all()
    return render(request, 'home.html', {"books": books})

@auth
def add_book(request):
    return render(request, 'add_book.html')

@auth
def view_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        type = request.POST['type']
        price = request.POST['price']
        book = Book()
        book.title = title
        book.type = type
        book.price = price
        book.save()
        return redirect('/home')

@auth
def edit_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        type = request.POST['type']
        price = request.POST['price']
        book = Book.objects.get(id=request.POST['bookid'])
        book.title = title
        book.type = type
        book.price = price
        book.save()
        return redirect('/home')
@auth
def edit_view_book(request):
    book = Book.objects.get(id=request.GET['bookid'])
    return render(request, 'edit_book.html',{"book": book})

@auth
def delete_book(request):
    book = Book.objects.get(id=request.GET['bookid'])
    book.delete()
    return redirect('/home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            username = request.POST['username']
            password = request.POST['password2']
            reader = Reader()
            reader.username = username
            reader.password = password
            reader.save()
            return redirect('/login')
    else:
        initial_data = {'username': '', 'password1': '', 'password2': ''}
        form = UserCreationForm(initial = initial_data)
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            username = Reader.username
            user.save()
            return redirect('/home', {"user" : username})
    else:
        initial_data = {'username': '', 'password': ''}
        form = AuthenticationForm(initial=initial_data)
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/login')