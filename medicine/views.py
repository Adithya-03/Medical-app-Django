from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login , logout
from .models import Medicine
from .forms import  Medicinedata
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required


# views.py


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # login(request, user)
#             # messages.success(request, 'You have successfully signed up.')
#             # return redirect('home')  # Replace 'home' with the name of your homepage URL
#             return render(request ,'login.html')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form': form})


from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect
 
def signup_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            # Redirect to login page after successful signup
            return redirect('log')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render,redirect
from django.contrib.auth import login 
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Authenticate the user
            user = form.get_user()
            login(request, user)
            # Redirect to home page after successful login
            return redirect('data')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
    # response = render(request, 'login.html', {'form': form})
    # response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    # response['Pragma'] = 'no-cache'
    # response['Expires'] = '0'
    # return response
    



# def login_view(request):
#     if request.user.is_authenticated:
#         return render(request, 'data.html')
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         print(user)
#         if user is not None:
#             login(request, user)
#             # return redirect ('data')
#             return render(request, 'data.html')

            
#         else:
#             msg = 'Error Login'
#             form = AuthenticationForm(request.POST)
#             return render(request, 'login.html', {'form': form, 'msg': msg})
#     else:
#         form = AuthenticationForm()
#         return render(request, 'login.html', {'form': form})
    
# def login_page(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('data')
#         else:
#             form = AuthenticationForm()
#             return render(request, 'login.html', {'form': form})
 

@login_required(login_url='/register/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def data(request):
    medicine_list=Medicine.objects.all()
    return render(request,'data.html',{'medicine_list':medicine_list})

@login_required(login_url='/register/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def  create(request):
    if request.method == 'POST':
        form =Medicinedata(request.POST)
        if form.is_valid():
            form.save()
            return redirect('data')
    else:
        form =Medicinedata()
    return render(request, 'create.html', {'form': form})


# def data(request):
#     medicine_list=Medicine.objects.all()
#     return render(request,'data.html',{'medicine_list':medicine_list})


# def update(request, id):
#     product = Medicine.objects.get(pk=id)
#     if request.method == 'POST':
#         form = Medicinedata(request.POST,instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('data')
#     else:
#         form =Medicinedata(instance=product)           
#     return render(request, 'edit.html', {'form': form})

from django.shortcuts import render, redirect
from .models import Medicine
from .forms import Medicinedata


@login_required(login_url='/register/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update(request, id):
    product = Medicine.objects.get(pk=id)
    if request.method == 'POST':
        form = Medicinedata(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('data')
    else:
        form = Medicinedata(instance=product)           
    return render(request, 'edit.html', {'form': form, 'product': product})



#delete 
@login_required(login_url='/register/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete(request,pk):
    medicine_list =Medicine.objects.get(pk=pk)  
    if request.method == 'POST':
        medicine_list.delete()
        return redirect('data')
    return render(request,'data.html',{'medicine_list': medicine_list})


# logout

# def logout(request):
#     return render(request,'entry.html')

def logout_view(request):
    logout(request)
    return redirect('register')


@login_required(login_url='/register/')
def search_view(request):
    if 'q' in request.GET:
        q = request.GET['q']
        # Construct a query to search for 'name' containing the search query
        search_query = Q(name__istartswith=q)
        
        # Filter Medicine objects based on the search query
        medicine_list = Medicine.objects.filter(search_query)
        context = {
            'medicine_list': medicine_list,
            'query': q,
        }
        return render(request, 'search_results.html', context)
    else:
        # If no search query provided, return an empty search page or handle it accordingly
        return render(request, 'data.html' )








