from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Validate user credentials
        user = User.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            # User credentials are valid, save user data in session variables
            request.session['user_id'] = user.pk
            request.session['username'] = user.username
            request.session['email'] = user.email
            return redirect('main')  # Replace 'main' with your desired URL
        else:
            messages.error(request, 'Invalid email or password.')
            pass

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        valid = True
        
        # Validate password strength using Django's built-in method
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password) or not any(char.islower() for char in password):
            messages.warning(request, "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, and one digit.")
            valid = False
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address.")
            valid = False
            
        # Check if the username is already taken using Django's built-in method
        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username taken.")
            valid = False
            
        if valid:
            # Create a new user using Django's built-in method
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request)
            # Redirect to the desired page
            return redirect('login')  # Replace 'login' with your actual login URL

    return render(request, 'register.html')

