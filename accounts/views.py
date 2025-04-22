from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib import auth
from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages
from .utils import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
# Create your views here.

# Restrict the vendor from accessig the customer dashboard and vice versa
def check_role_vendor(user):
  if user.role == 1:
    return True
  else:
    raise PermissionDenied
def check_role_customer(user):
  if user.role == 2:
    return True
  else:
    raise PermissionDenied
  
def registerUser(request):
  if request.user.is_authenticated:
    messages.warning(request, "You are already logged in")
    return redirect('myAccount')
  # sourcery skip: extract-method, remove-unnecessary-else
  elif request.method == 'POST':
    form = UserForm(request.POST)    
    if form.is_valid():
      # Method 1: Create the user using the form data
      password = form.cleaned_data.get('password')
      user = form.save(commit=False) # coommit false is used to not save the user yet
      user.set_password(password) # set the password instead of saving it in plain text (hash format)
      user.role = User.CUSTOMER
      user.save()
      
      # Method 2: Create the user using the create_user method
      # first_name = form.cleaned_data.get('first_name')
      # last_name = form.cleaned_data.get('last_name')
      # username = form.cleaned_data.get('username')
      # email = form.cleaned_data.get('email')
      # password = form.cleaned_data.get('password')
      # user = User.objects.create_user(
      #   first_name=first_name,
      #   last_name=last_name,
      #   username=username,
      #   email=email,
      #   password=password,
      # )
      # user.role = User.CUSTOMER
      # user.save()

      # print("User Created")
      messages.success(request, "Account has been Created Successfully")
      return redirect('registerUser')
    else:
      print("Form is not valid")
      print(form.errors)
  else :
    form = UserForm()

  context = {
    'form': form,
  }
  return render(request,'accounts/registerUser.html', context)

def registerVendor(request):
  if request.user.is_authenticated:
    messages.warning(request, "You are already logged in")
    return redirect('dashboard')
  # sourcery skip: extract-method, remove-unnecessary-else
  elif request.method=='POST':
    form = UserForm(request.POST)
    v_form = VendorForm(request.POST, request.FILES)
    if form.is_valid() and v_form.is_valid():
      # Method 1: Create the user using the form data
      password = form.cleaned_data.get('password')
      user = form.save(commit=False)
      user.set_password(password)
      user.role = User.VENDOR
      user.save()

      vendor = v_form.save(commit=False)
      vendor.user = user
      user_profile = UserProfile.objects.get(user=user) 
      vendor.user_profile = user_profile
      vendor.save()

      messages.success(request, "Vendor Account has been Created Successfully! Please wait for approval.")
      return redirect('registerVendor')
    else:
      print("Form is not valid")
      print(form.errors)
  else:
      form = UserForm()
      v_form = VendorForm()
  context = {
    'form': form,
    'v_form': v_form,
  }
  return render(request,'accounts/registerVendor.html',context)

def login(request):
  if request.user.is_authenticated:
    messages.warning(request, "You are already logged in")
    return redirect('myAccount')
  
  elif request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate(request, username=email, password=password)
    if user is not None:
      # Login the user
      auth.login(request, user)
      messages.success(request, "Login Successful")
      return redirect('myAccount')
    else:
      messages.error(request, "Invalid Credentials")
      return redirect('login')
    
    # try:
    #   user = User.objects.get(username=email)
    #   if user.check_password(password):
    #     # Login the user
    #     messages.success(request, "Login Successful")
    #     return redirect('dashboard')
    #   else:
    #     messages.error(request, "Invalid Password")
    # except User.DoesNotExist:
    #   messages.error(request, "User does not exist")

  return render(request,'accounts/login.html')

def logout(request):
  auth.logout(request)
  messages.info(request, "Logged out successfully")
  return redirect('login')

@login_required(login_url='login')

def myAccount(request):
  user = request.user
  redirectUrl = detectUser(user)
  return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
  return render(request,'accounts/customerDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
  return render(request,'accounts/vendorDashboard.html')