from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from rb_pages.models import Favorite, Species


def is_email(s):
    try:
        validate_email(s)
        return True
    except ValidationError:
        return False


def login_view(request):
    if request.method == "POST":
        user_or_email = request.POST.get("user_or_email")
        password = request.POST.get("password")

        if is_email(user_or_email):
            username = User.objects.get(email=user_or_email).username
            user = authenticate(request, username=username, password=password)
        else:
            user = authenticate(request, username=user_or_email, password=password)

        if user is not None:
            # Authentication succeeded, log in the user
            login(request, user)
            return redirect("main")  # Replace 'main' with your desired URL
        else:
            # Authentication failed
            messages.error(request, "Invalid email or password.")

    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("landing")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        valid = True

        # Validate password strength using Django's built-in method
        if (
            len(password) < 8
            or not any(char.isdigit() for char in password)
            or not any(char.isupper() for char in password)
            or not any(char.islower() for char in password)
        ):
            messages.warning(
                request,
                "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, and one digit.",
            )
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
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            login(request, user)
            # Redirect to the desired page
            return redirect("main")  # Replace 'login' with your actual login URL

    return render(request, "register.html")


def landing_view(request):
    return render(request, "landing.html", {"user": request.user})


@login_required
def main_view(request):
    user = request.user
    species_data = Species.objects.all()
    is_user_admin = user.is_superuser  # Assuming admin users are superusers in Django

    if request.method == "GET" and "search" in request.GET:
        search_query = request.GET.get("query").lower()
        species_data = Species.objects.filter(name__icontains=search_query)

    user_favorites = Species.objects.filter(favorite__user=user).distinct()
    
    return render(
        request,
        "main.html",
        {"species_data": species_data, "is_user_admin": is_user_admin, "user_favorites": user_favorites},
    )


@login_required
def toggle_favorite(request, species_id):
    user = request.user
    species = Species.objects.get(id=species_id)
    is_favorited = Favorite.objects.filter(user=user, species=species).exists()

    if is_favorited:
        Favorite.objects.filter(user=user, species=species).delete()
    else:
        Favorite.objects.create(user=user, species=species)

    return redirect("main")
