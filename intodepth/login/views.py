from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from .utils import is_alpha, is_alphanumeric
from .models import mystudent


# custom functions
import re
def is_alpha_with_spaces(string):
    # Remove all non-alphabetic characters
    filtered_string = re.sub(r'[^a-zA-Z]', '', '_', string)
    return filtered_string.isalpha()






# Create your views here.

def home(request):
    #return HttpResponse("Hello world")
    return render(request, 'login.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if user.is_superuser:
                return redirect('user_home')
            else:
                return redirect('user_home')          
            
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')
    

@login_required(login_url='login')
def super(request):
        context = {
            'fname': request.user.first_name,
            'lname': request.user.last_name,
            'username': request.user.username
        }
        
        return render(request, 'super.html', context)


@login_required(login_url='login')
def user_home(request):
        
        
        context = {
            'firstname': request.user.first_name,
            'lastname': request.user.last_name
            
        }
        return render(request, 'user_home.html', context)
 


def logout_view(request):
    logout(request)
    return redirect('login')





def register(request):
    if request.method == 'POST':
         first_name = request.POST['firstname']
         last_name = request.POST['lastname']
         username = request.POST['username']
         email = request.POST['email']
         password1 = request.POST['password1']
         password2 = request.POST['password2']

         if password1 == password2 and is_alpha(first_name) and is_alpha(last_name) and is_alphanumeric(username):
              if User.objects.filter(username=username).exists():
                   print(f"User name {username}is taken")
                   messages.info(request, 'The username is taken')
                   return redirect('register')
              elif User.objects.filter(email=email).exists():
                   print(f"Email {email}is taken")
                   messages.info(request, 'The email is taken')
                   return redirect('register')
              else:
                   user = User.objects.create_user(username=username, password=password1, first_name=first_name, last_name=last_name, email=email)
                   user.save()
                   messages.info(request, f"Congratulations. Account created!")
                   return redirect('login')
         else:
              
              messages.info(request, 'Form validation failed!')
              return redirect('register')
         
    else:
        return render(request, 'register.html')
    



@login_required(login_url='login')
def profile(request, username):
     user = get_object_or_404(User, username=username)
     context = {
          'username': user.username,
          'firstname': user.first_name,
          'lastname': user.last_name,
          'email': user.email

     }
   
     return render(request, 'profile.html', context)


@login_required(login_url='login')
def edit_profile(request, username):
     user = get_object_or_404(User, username=username)
     if request.method == "POST":
          form = UserForm(request.POST, instance=user)
          if form.is_valid():
               form.save()
               messages.success(request, "Profile updated !!!!")
               return redirect('user_home')       
     else:
          form = UserForm(instance=user)
          firstname = user.first_name
          return render(request, 'edit_profile.html', {'form':form, 'firstname':firstname})
         



@login_required(login_url='login')
def reset_password(request, username):
     u = User.objects.get(username=username)
     if request.method == "POST":
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        

        if password1 == password2:
             
             u.set_password(password1)
             u.save()
             messages.info(request, "Password updated. Please login using the new password!")
             return redirect('logout')
        else:
             messages.info(request, "Password do not match!!!")
             return render(request, 'reset_password.html')

    
     else:
          firstname = u.first_name
          return render(request, 'reset_password.html', {'firstname':firstname})
     

@login_required(login_url='login')    
def manage_user(request):
     firstname = request.user.first_name
     return render(request, 'manage_user.html', {'firstname':firstname})

def forgot (request):
     messages.info(request, "Please forward your username to admin@home.com to reset password")
     return redirect('login')



@login_required(login_url='login')
def admin_alluser(request):

     if request.user.is_superuser:
          obj = User.objects.all().order_by('-is_superuser').values()
          user_count = User.objects.count()
          superuser_count = User.objects.filter(is_superuser=True).count()
          firstname = request.user.first_name
          return render(request, 'admin_alluser.html', {'obj':obj, 'firstname':firstname, 'count':user_count, 'superuser_count':superuser_count})

     else:

          return redirect('login')
     


@login_required(login_url='login')
def admin_editprofile(request, username):
     user = get_object_or_404(User, username=username)
     if request.method == "POST":
          form = UserForm(request.POST, instance=user)
          if form.is_valid():
               form.save()
               messages.success(request, f"{username} Profile updated !!!!")
               return redirect('admin_alluser')
     else:
          form = UserForm(instance=user)
     firstname = user.first_name
     return render(request, 'admin_editprofile.html', {'form':form, 'firstname':firstname})




@login_required(login_url='login')
def change_role(request):

     if request.method == "POST":


          username = request.POST['username']
          role = request.POST['role']

          if username == request.user.username:
               messages.info(request, "Cannot change currentely logged in user role")
               return redirect('change_role')
          else:

               try:
                    user = User.objects.get(username=username)

                    if role == "superuser":
                         user.is_superuser = True
                    else:
                         user.is_superuser = False
                    user.save()
                    messages.info(request, f"{username} role changed to {role}")
                    
               except User.DoesNotExist:
                    messages.info(request, f"{username} does not exist")

               return redirect('change_role')
                 
          
     else:
          usernames = User.objects.values_list('username', flat=True)

          firstname = request.user.first_name
          return render(request, 'change_role.html', {'firstname':firstname, 'usernames':usernames})
     


@login_required(login_url='login')
def admin_passreset(request):

     if request.method == "POST":
          username = request.POST['username']
          password1 = request.POST['password1']
          password2 = request.POST['password2']

          if password1 == password2:
               try:
                    user = User.objects.get(username=username)
                    user.set_password(password1)
                    user.save()
                    messages.info(request, f"{username} New password is : {password1}")
               except User.DoesNotExist:
                    messages.info(request, "User does not exist")
               
               return redirect('admin_passreset')
          else:
               messages.info(request, "Password do not match!")
               return redirect('admin_passreset')

     else:
          usernames = User.objects.values_list('username', flat=True)
                    
          firstname = request.user.first_name
          return render(request, 'admin_passreset.html', {'firstname':firstname, 'usernames':usernames})
     




@login_required(login_url='login')
def add_user(request):
     if request.method == 'POST':
         first_name = request.POST['firstname']
         last_name = request.POST['lastname']
         username = request.POST['username']
         email = request.POST['email']
         password1 = request.POST['password1']
         password2 = request.POST['password2']

         if password1 == password2 and is_alpha(first_name) and is_alpha(last_name) and is_alphanumeric(username):
              if User.objects.filter(username=username).exists():
                   print(f"User name {username}is taken")
                   messages.info(request, 'The username is taken')
                   return redirect('add_user')
              elif User.objects.filter(email=email).exists():
                   print(f"Email {email}is taken")
                   messages.info(request, 'The email is taken')
                   return redirect('add_user')
              else:
                   user = User.objects.create_user(username=username, password=password1, first_name=first_name, last_name=last_name, email=email)
                   user.save()
                   messages.info(request, f"Congratulations. Account created!")
                   return redirect('add_user')
         else:
              
              messages.info(request, 'Form validation failed!')
              return redirect('add_user')
         
     else:
          return render(request, 'add_user.html')


        


@login_required(login_url='login')
def delete_user(request):

     if request.method == "POST":
          username = request.POST['username']
          user = get_object_or_404(User, username=username)
          user.delete()
          messages.info(request, "User deleted")
          return redirect('delete_user')


 
     else:
          usernames = User.objects.values_list('username', flat=True)

          firstname = request.user.first_name
          return render(request, 'delete_user.html', {'firstname': firstname, 'usernames':usernames})
     

def test(request):
     #obj = get_object_or_404(mystudent, id=1)
     obj = mystudent.objects.get(id=1)
     obj1 = request.session


     context = {
          'obj1': obj1,
          'obj': obj,
          'name': 'jabbar',
          'pro': "IT"
     }
     return render(request, 'test.html', context)
     
          
