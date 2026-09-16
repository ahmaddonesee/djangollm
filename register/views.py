from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.models import User
from .forms import AdminSignUpForm
# Create your views here.


from django.shortcuts import render, redirect
from .forms import AdminSignUpForm


def admin_signup(request):

    if request.method == "POST":
        form = AdminSignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data["password1"]
            )

            # User can access Django Admin
            user.is_admin = True
            # user.is_staff = True

            # Save user
            user.save()

            return redirect("admin:login")

    else:
        form = AdminSignUpForm()

    return render(
        request,
        "admin/signup.html",
        {"form": form}
    )




def  register(request):
    form = AdminSignUpForm()
    if request.method=="POST":
        form=AdminSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request,user)
            return redirect('llm:upload_file')
    else:
        return  render(request,'register/register.html',{'form':form})    

def login_view(request):
    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST)
        if  form.is_valid():
            user_name=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=user_name,password=password)
            if user  is not None :
                user.save()
                login(request,user)
                messages.info(request, f"You are now logged in as {user_name}.")
                return redirect('llm:upload_file')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form=AuthenticationForm()
    return render(request,'register/login.html',{'form':form}) 
        
     
def logout_view(request):
    logout(request)
    messages.info(request,"Logged out successfully!")
    return redirect("llm:upload_file")


def delete_account(request,id):
    user=User.objects.get(id=id)
    if request.method=="POST":
        user.delete()
        messages.success(request,"Account Deleted Successfully")
        return redirect('llm:upload_file')
    return render(request,'register/delete_account.html',{"user":user}) 


# def 