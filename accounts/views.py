from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import UserForm
from .models import User
from django.contrib import messages
# Create your views here.
def registerUser(request):
  # sourcery skip: extract-method, remove-unnecessary-else
  if request.method == 'POST':
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
