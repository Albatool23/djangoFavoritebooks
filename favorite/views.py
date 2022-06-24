from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == 'POST':
        errors = Users.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            request.session['users_id'] = Users.objects.get(email=request.POST['email']).id
            print (request.session['users_id'])
            return redirect('/addBook')

def register(request):
    if request.method == 'POST':
        errors = Users.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            newUser = Users.objects.create(
                fname = request.POST['fname'],
                lname=request.POST['lname'],
                email = request.POST['email'],
                password = hash
            )
            newUser.save()
            request.session['users_id'] = newUser.id
            return redirect('/')


def signout(request):
    del request.session['users_id']
    print(request.session.values())
    return redirect("/")


def addBook(request):
    if not 'users_id' in request.session:
        print("test add book")
        return redirect('/')
    if request.method == 'POST':
        errors = Books.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/addBook')
        else:
            title = request.POST['title']
            desc = request.POST['desc']
            user = Users.objects.get(id=request.session['users_id'])
            newBook = Books.objects.create(title=title, desc=desc, user=user)
            newBook.like.add(user)
            newBook.save()
            return redirect('/addBook')

    books = Books.objects.all()
    user = Users.objects.get(id=request.session['users_id'])
    print("Logged in as", user.fname)
    context = {
            "books": books,
            "user": user
    }

    return render(request, "addbook.html", context)



def displybook(request, ID):
    book = Books.objects.get(id=ID)
    user = Users.objects.get(id=request.session['users_id'])
    print("Logged in as", user)
    context = {
        "book": book,
        "user": user
    }
    return render(request, "displybook.html", context)




def edit(request):
    if request.method == 'POST' and 'add' in request.POST:
        ID = request.POST['id']
        errors = Books.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/displybook/{ID}')
        else:
            title = request.POST['title']
            desc = request.POST['desc']
            book = Books.objects.get(id=ID)
            book.title = title
            book.desc = desc
            book.save()
            return redirect(f'/displybook/{ID}')
    if request.method == 'POST' and 'delete' in request.POST:
        ID = request.POST['id']
        book = Books.objects.get(id=ID)
        book.delete()
        return redirect('/addBook')



def Favorite(request, ID):
    book = Books.objects.get(id=ID)
    user = Users.objects.get(id=request.session['users_id'])
    user.liked_books.add(book)
    return redirect(f'/displybook/{ID}')

def unFavorite(request, ID):
    book = Books.objects.get(id=ID)
    user = Users.objects.get(id=request.session['users_id'])
    user.Favorite.remove(book)
    return redirect(f'/displybook/{ID}')



