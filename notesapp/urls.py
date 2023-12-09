from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import index, new_note, note_detail, delete_note,  signup, about, profile, change_password

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Redirect to login page after logout
    path('signup/', views.signup, name='signup'),
    path('password_change/', change_password, name='password_change'),
    path('', views.index, name = 'index'),
    path('about', views.about, name = 'about'),
    path('profile', views.profile, name = 'profile'),
    path('new_note', views.new_note, name = 'new'),
    path('note/<str:pk>', views.note_detail, name = 'note'),
    path('note/<int:pk>/', views.note_detail, name='note'),
    path('delete_note/<str:pk>', views.delete_note, name = 'delete'),
    

]