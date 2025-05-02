from django.shortcuts import render,get_object_or_404,redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm 
from accounts.models import UserProfile 
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category,Product
from menu.forms import CategoryForm,ProductForm
from django.template.defaultfilters import slugify
# Helper function
def get_vendor(request):
  vendor = Vendor.objects.get(user=request.user)
  return vendor
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
  profile = get_object_or_404(UserProfile, user=request.user)
  vendor = get_object_or_404(Vendor, user=request.user)

  if request.method == 'POST':
    profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
    vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)

    if profile_form.is_valid() and vendor_form.is_valid():
      profile_form.save()
      vendor_form.save()
      # messages.success(request, "Settings updated successfully!")
      return redirect('vprofile')
    else:
      print("Form is not valid")
      print(profile_form.errors)
      print(vendor_form.errors)
  else:
    # Pre-fill the forms with the current user's data
    profile_form = UserProfileForm(instance=profile)
    vendor_form = VendorForm(instance=vendor)

  context = {
      'profile': profile,
      'vendor': vendor,
      'profile_form': profile_form,
      'vendor_form': vendor_form,
  }
  return render(request, 'vendor/vprofile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
  vendor = get_vendor(request)
  categories = Category.objects.filter(vendor=vendor).order_by('created_at')  
  context = {
      'categories': categories,
  }
  return render(request, 'vendor/menu_builder.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
  vendor = get_vendor(request)
  categories = Category.objects.filter(vendor=vendor)
  category = get_object_or_404(Category, pk=pk)
  fooditems = Product.objects.filter(category=category, vendor=vendor)
  print(fooditems)
  context = {
      'categories': categories,
      'category': category,
      'fooditems': fooditems,
  }
  return render(request, 'vendor/fooditems_by_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    if form.is_valid():
      category_name = form.cleaned_data['category_name']
      category = form.save(commit=False)
      category.vendor = get_vendor(request)
      category.slug = slugify(category_name)
      category.save()
      messages.success(request, "Category added successfully!")
      return redirect('menu_builder')
    else:
      print("Form is not valid")
      print(form.errors)
  else:
    form = CategoryForm()
  context ={
      'form': form,
  }
  return render(request, 'vendor/add_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk):
  category = get_object_or_404(Category, pk=pk)
  if request.method == 'POST':
    form = CategoryForm(request.POST, instance=category)
    if form.is_valid():
      category_name = form.cleaned_data['category_name']
      category.slug = slugify(category_name)
      form.save()
      messages.success(request, "Category updated successfully!")
      return redirect('menu_builder')
    else:
      print("Form is not valid")
      print(form.errors)
  else:
    form = CategoryForm(instance=category)
  context ={
      'category': category,
      'form': form,
  }
  return render(request, 'vendor/edit_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk):
  category = get_object_or_404(Category, pk=pk)
  category.delete()
  messages.success(request, "Category deleted successfully!")
  return redirect('menu_builder')
  

# FoodItems Crud
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    vendor = get_vendor(request)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']

            if Product.objects.filter(vendor=vendor, product_name__iexact=product_name).exists():
                form.add_error('product_name', 'The product with same name already exists.')
            else:
                fooditem = form.save(commit=False)
                fooditem.vendor = vendor
                fooditem.slug = slugify(product_name)
                fooditem.save()
                messages.success(request, "Food item added successfully!")
                return redirect('fooditems_by_category', pk=fooditem.category.pk)
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = ProductForm()
        # To show the categories of the loggedin vendor in the dropdown
        form.fields['category'].queryset = Category.objects.filter(vendor=vendor)
    context = {'form': form}
    return render(request, 'vendor/add_food.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request, pk):
  vendor = get_vendor(request)
  fooditem = get_object_or_404(Product, pk=pk)
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES, instance=fooditem)
    if form.is_valid():
      form.save()
      messages.success(request, "Food item updated successfully!")
      return redirect('fooditems_by_category', pk=fooditem.category.pk)
    else:
      print("Form is not valid")
      print(form.errors)
  else:
    form = ProductForm(instance=fooditem)
    form.fields['category'].queryset = Category.objects.filter(vendor=vendor)

  context ={
      'fooditem': fooditem,
      'form': form,
  }
  return render(request, 'vendor/edit_food.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request, pk):
  fooditem = get_object_or_404(Product, pk=pk)
  fooditem.delete()
  messages.success(request, "Food item deleted successfully!")
  return redirect('fooditems_by_category', pk=fooditem.category.pk)