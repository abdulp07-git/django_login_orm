from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from .models import website_user

# Create your views here.

def home(request):
    #return HttpResponse("Hello world")
    return render(request, 'login.html')



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = website_user.objects.get(username=username)
            if check_password(password, user.password):
                # Create a user object with the authenticated user details
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth_login(request, user)
                return redirect('home')  # Redirect to a success page
            else:
                return HttpResponse('Invalid password')
        except website_user.DoesNotExist:
            return HttpResponse('Invalid username')

    return render(request, 'login.html')






def register(request):

    context = {
        'name': 'abdul',
        'age': 37
    }
    return render(request, 'register.html', context)

def user(request):
    return render(request, 'user.html')

def super(request):
    return render(request, 'super.html')
