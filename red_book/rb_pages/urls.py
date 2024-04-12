from django.urls import path
from rb_pages.views import login_view, logout_view, register_view, landing_view, toggle_favorite, main_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('', landing_view, name='landing'),
    path("main/", main_view, name='main'),
    path("logout/", logout_view, name="logout"),
    path('toggle_favorite/<int:species_id>/', toggle_favorite, name='toggle_favorite'),
    
]