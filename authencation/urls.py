from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name="user_login"),
    path('user_signup', views.user_signup, name="user_signup"),
    path('user_logout', views.user_logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('activate_account/<uidb64>/<token>', views.VarificationView, name='activate_account'),
]