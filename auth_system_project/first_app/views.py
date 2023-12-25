from django.shortcuts import render, redirect
from .forms import SignUpForm, EditProfileForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm 
from django.contrib import messages

# Create your views here.
def sign_up(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Your account has been created successfully')
                form.save()
                return redirect('log_in')
        else:
            form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
    else:
        return redirect('profile')
    
def log_in(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request= request, data= request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                pswrd = form.cleaned_data['password']
                user = authenticate(username= name, password= pswrd)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login successful')
                    return redirect('profile')
        else:
            form = AuthenticationForm()
        return render(request,'login.html',{'form':form})
    else:
        return redirect('profile')
    

def profile(request):
    if request.user.is_authenticated:
        return render(request,'profile.html')
    else:
        return redirect('log_in')


def log_out(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('homepage')

def cng_pswd1(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SetPasswordForm(user = request.user , data= request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password updated without using old password successfully')
                return redirect('profile')
        else:
            form = SetPasswordForm(user = request.user)
        return render(request, 'changepassword.html', {'form': form})
    else:
        return redirect('log_in')
    

def cng_pswd2(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user = request.user , data= request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password updated using old password successfully')
                return redirect('profile')
        else:
            form = PasswordChangeForm(user= request.user)
        return render(request, 'changepassword.html', {'form': form})
    else:
        return redirect('log_in')