from django.urls import path
from . import views


urlpatterns = [

    path('',views.signup_func,name='signuppage'),
    path('loginpage/',views.login_func,name='loginpage'),
    path('logoutpage/',views.logout_func,name='logoutpage')

]

