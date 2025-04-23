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
from django.utils.http import urlsafe_base64_decode
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
      # Send Verification Email
      mail_subject = "Activate your Customer account"
      email_template = "accounts/emails/account_verification_email.html"
      send_verification_email(request, user,mail_subject,email_template)
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
      mail_subject = "Activate your vendor account"
      email_template = "accounts/emails/account_verification_email.html"
      send_verification_email(request, user,mail_subject,email_template)
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

def activate(request, uidb64, token):
  # activate the user by setting the is_active field to True
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None

  if user is not None and default_token_generator.check_token(user, token):
    user.is_active = True
    user.save()
    messages.success(request, "Congratulations!! Account activated successfully")
    return redirect('login')
  else:
    messages.error(request, "Activation link is invalid!")
    return redirect('login')
  

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

def forgotPassword(request):  # sourcery skip: extract-method
  if request.method == 'POST':
    email = request.POST.get('email')
    try:
      user = User.objects.get(email=email)
      mail_subject = "Reset your password"
      email_template = "accounts/emails/resetPasswordEmail.html"
      send_verification_email(request, user, mail_subject,email_template)
      messages.success(request, "Password reset email has been sent to your email address")
      return redirect('login')
    except User.DoesNotExist:
      messages.error(request, "User does not exist")
      return redirect('forgotPassword')
  return render(request,'accounts/forgotPassword.html')

def resetPasswordValidate(request, uidb64, token):
   # validate the user by checking the token  
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User._default_manager.get(pk=uid)
  except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  
  if user is not None and default_token_generator.check_token(user, token):
    request.session['uid'] = uid
    messages.info(request, "Please reset your password")
    return redirect('resetPassword')
  else:
    messages.error(request, "Password reset link is expired")
    return redirect('login')

def resetPassword(request):
  if request.method == 'POST':
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    if password == confirm_password:
      try:
        pk = request.session.get('uid')
        user = User.objects.get(pk=pk)
        user.set_password(password)
        user.is_active = True
        user.save()
        messages.success(request, "Password reset successfully")
        return redirect('login')
      except User.DoesNotExist:
        messages.error(request, "User does not exist")
        return redirect('resetPassword')
    else:
      messages.error(request, "Passwords do not match")
      return redirect('resetPassword')
  return render(request,'accounts/resetPassword.html')