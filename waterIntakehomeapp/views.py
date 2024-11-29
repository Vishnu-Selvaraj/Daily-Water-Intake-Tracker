from django.shortcuts import render ,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout

# Create your views here.

def signup_func(request):
    if request.POST:
        form = UserCreationForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('loginpage')
          
    else:
        form = UserCreationForm()
    return render(request,'signupform.html',{'form':form})

def login_func(request):
    error = None
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('add')
        else:
            error = 'Invalid Username or Password'
    else:
        form = AuthenticationForm()
    return render(request,'loginform.html',{'form':form,'error':error})

def logout_func(request):
    if request.method == 'GET':
        logout(request)
        return redirect('loginpage')
    else:
        return redirect('/loginpage')
        

            

