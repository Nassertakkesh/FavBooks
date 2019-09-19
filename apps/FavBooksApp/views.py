
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        print(password)
        password_confirm = request.POST['password_confirm']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) 
        pw_hash_confirm = bcrypt.hashpw(password_confirm.encode(), bcrypt.gensalt()) 
        print(pw_hash)
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=pw_hash, password_confirm=pw_hash_confirm, 
        email=request.POST['email'], birth_date=request.POST['birth_date']) 
        print("its working")

        return redirect("/book")
        
def login(request):
    if not User.objects.loginValid(request):
        return redirect('/')
    else:
        theuser = User.objects.filter(email=request.POST['email']) 
        if theuser: 
            logged_user = theuser[0] 
            request.session['userid'] = logged_user.id
            return redirect('/book')
        return redirect('/')

def index(request):
    if request.session.get("userid"):
        return redirect("/book")
    return render(request,"FavBooksApp/index.html")

def presuccess(request):
    uid = request.session.get("userid")
    if not uid:
        return redirect("/")
    context = {
        "thisuser" : User.objects.get(id=uid),
        "allbooks" : Book.objects.all(),
        "this_user" : User.objects.get(id=uid)


        
    }
    return render(request,"FavBooksApp/success.html",context)

def logout(request):
    del request.session['userid'] 
    return redirect("/")

################^^^^^^^^^^^THE ABOVE CODE IS FOR REGISTRATION AND LOGIN^^^^^^^^^^^^######################

def addingbook(request):
    errors = User.objects.book_add_valid(request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/book')
    else:
        if request.session.get("userid"):
            this_user_session_id= request.session.get("userid")
            print(this_user_session_id)
            this_user_obj= User.objects.get(id= this_user_session_id)
            print(this_user_obj.first_name)
            # print(for key in )
            new_book_adding = Book.objects.create(title=request.POST["titleName"],desc=request.POST["descriptionName"],uploaded_by = this_user_obj)
            print(new_book_adding)
            this_user = User.objects.get(id=this_user_session_id)
            print(this_user)
            new_book_adding.users_who_fav.add(this_user)
            return redirect ("/book")
        return render(request,"FavBooksApp/index.html")

def favorite(request,id):
    if request.session.get("userid"):
        the_book_being_liked= id
        this_user_session_id= request.session.get("userid")
        this_book = Book.objects.get(id=the_book_being_liked)
        this_user = User.objects.get(id=this_user_session_id)
        print(this_book)
        print(this_user)
        print(this_user_session_id)
        print(the_book_being_liked)
        this_book.users_who_fav.add(this_user)

        return redirect ("/book") 
    return render(request,"FavBooksApp/index.html")



def books_page(request,id):
    if request.session.get("userid"):
        the_book_being_liked= id
        this_user_session_id= request.session.get("userid")
        this_book = Book.objects.get(id=the_book_being_liked)
        this_user = User.objects.get(id=this_user_session_id)
        context={
            "book": Book.objects.get(id=id),
            "users": User.objects.all(),
            "users_header": this_user,
            "users_fav":this_book.users_who_fav.all()
        }

        return render(request,"FavBooksApp/books_page.html",context)
    return render(request,"FavBooksApp/index.html")


def unfavorite(request,id):
    if request.session.get("userid"):
        the_book_being_liked= id
        this_user_session_id= request.session.get("userid")
        this_book = Book.objects.get(id=the_book_being_liked)
        this_user = User.objects.get(id=this_user_session_id)
        print(this_book)
        print(this_user)
        print(this_user_session_id)
        print(the_book_being_liked)
        this_book.users_who_fav.remove(this_user)
        # print("lets see this")
        # the_book_being_liked= id
        # this_user_session_id= request.session.get("userid")
        # the_user_final= User.objects.get(id=this_user_session_id)
        
        # print("lets see this")
        # if the_user_final in users_that_fav.books_liked.all():
        #     # (id=this_user_session_id):
        #     print("KJBKJ KJNJKBKJBKJNBKJNKNKBNKJN ")
        #     this_book = Book.objects.get(id=the_book_being_liked)
        #     this_user = User.objects.get(id=this_user_session_id)
        #     this_book.users_who_fav.remove(this_user)
        return redirect ("/book") 
    return render(request,"FavBooksApp/index.html")

def editbook(request,id):
    errors = User.objects.book_add_valid(request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/book')
    else:
        if request.session.get("userid"):
            the_book_being_edited= id
            this_book = Book.objects.get(id=the_book_being_edited)
            this_book.title = request.POST['titleName']
            this_book.desc = request.POST['descriptionName']
            this_book.save()

            return redirect('/book')
    return render(request,"FavBooksApp/index.html")

def delete(request,id):
        if request.session.get("userid"):
            the_book_being_deleted= id
            this_book = Book.objects.get(id=the_book_being_deleted)
            this_book.delete()
            return redirect('/book')
        return render(request,"FavBooksApp/index.html")



def fav_books(request):
    if request.session.get("userid"):
        this_user_session_id= request.session.get("userid")
        this_user= User.objects.get(id=this_user_session_id)

        context={
            "users": this_user.books_liked.all(),
            "this_user": this_user
        }

        return render(request,"FavBooksApp/favs.html",context)
    return render(request,"FavBooksApp/index.html")
    #  if request.session.get("userid") == Book.objects.uploaded_by.get(id=id):
    #         the_book_being_liked= id
    #         this_user_session_id= request.session.get("userid")
    #         this_book = Book.objects.get(id=the_book_being_liked)
    #         this_user = User.objects.get(id=this_user_session_id)
    #         context={
    #             "book": Book.objects.get(id=id),
    #             "users": User.objects.all(),
    #             "users_header": this_user,
    #             "users_fav":this_book.users_who_fav.all()
    #         }

    #     else:




