from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone




#Employee page to Register employee and show the employee list based on company
@login_required(login_url='/login/')
def employee(request):
    if request.method == "POST":
        employee_name = request.POST.get('employee_name')
        employee_position = request.POST.get('employee_position')

        Employee.objects.create(

            #create unique employee_id base on company user name
            employee_id = len(Employee.objects.all().filter(employee_comp_name=request.user))+1,

            employee_name = employee_name,
            employee_position = employee_position,
            employee_comp_name = request.user,
        )
        return redirect('/')

    #to show all objects of Employee based on company_username
    queryset = Employee.objects.all().filter(employee_comp_name=request.user)
    context = {'employees' : queryset}

    return render(request, 'employee.html', context)




# device page to register device, show the Device table objects and allocate or deallocate device to employee
@login_required(login_url='/login/')
def device(request):
    if request.method == "POST":
        device_model = request.POST.get('device_model')
        device_type = request.POST.get('device_type')
        device_condition = request.POST.get('device_condition')

        
        Device.objects.create(
            #create unique device_id base on company user name
            device_id = len(Device.objects.all().filter(device_comp_name=request.user))+1,

            device_model = device_model,
            device_type = device_type,
            device_condition = device_condition,
            device_comp_name = request.user,
        )

        return redirect('/device/')

    #to show all objects of Device based on company_username
    queryset = Device.objects.all().filter(device_comp_name=request.user)
    context = {'devices' : queryset}

    return render(request, 'device.html', context)




#checkout page redirect from device page to checkout a device and allocate to a employee
@login_required(login_url='/login/')
def check_out(request, id):
    if request.method == "POST":
        _condition = request.POST.get('_condition')
        _employee_id = request.POST.get('_employee_id')


        #cehck for valid employee_id for this company
        queryset = Employee.objects.all().filter(employee_comp_name = request.user, employee_id = _employee_id)
        if len(queryset) == 0:
            messages.info(request, "Invalid Employee Id")
            return render(request, 'checkoutform.html')

        #update the query and allocate the device to employee using his/her id
        queryset = Device.objects.get(id = id)
        queryset.device_occupied_by = int(_employee_id)
        queryset.save()


        #Collecting DeviceLogInformation data
        DeviceLogInfo.objects.create(
            device_id = queryset.device_id,
            device_comp_name = queryset.device_comp_name,
            device_occupied_by = int(_employee_id),
            device_checkout_time = timezone.now(),
            device_checkout_condition = _condition,
        )
        return redirect('/device')
    return render(request, 'checkoutform.html')





#return_back page redirect from device page to return back a device
@login_required(login_url='/login/')
def return_back(request, id):
    if request.method == "POST":
        _condition = request.POST.get('_condition')
        queryset = Device.objects.get(id = id)
        queryset.device_occupied_by = 0
        queryset.save()


        #update devicesLogInformation table with return time data
        log_queryset = DeviceLogInfo.objects.all().filter(device_id = queryset.device_id).latest('id')
        log_queryset.device_return_back_time = timezone.now()
        log_queryset.device_return_back_condition = _condition
        log_queryset.save()


        return redirect('/device/')
    return render(request, 'returnform.html')



#viewing devices log history based on company username
@login_required(login_url='/login/')
def device_log(request):
    #Search device Log history by its id
    if request.method == "POST":
        search_device_id = request.POST.get('search_device_id')
        queryset = DeviceLogInfo.objects.all().filter(device_comp_name=request.user, device_id = search_device_id)
        context = {'devices' : queryset}
        return render(request, 'devicelog.html', context)
    

    queryset = DeviceLogInfo.objects.all().filter(device_comp_name=request.user)
    context = {'devices' : queryset}
    return render(request, 'devicelog.html', context)





#log in page for company
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')


        #check for valid username
        user = User.objects.filter(username = username)
        if not user.exists():
            messages.info(request, "Invalid Username")
            return redirect('/login/')
        
        # authenticate username and password
        user = authenticate(username = username , password = password)


        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')




#logout page
@login_required(login_url='/login/')
def logout_page(request):
    logout(request)
    return redirect('/login/')




#Registration page
def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        password = request.POST.get('password')


        #check for this username already exists or not
        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, "Username already taken")
            return redirect('/register/')

        #create a user
        user = User.objects.create(
            first_name = first_name,
            username = username,
        )
        user.set_password(password)
        user.save()

        messages.info(request, "Account created successfully")
        return redirect('/register/')
    return render(request, 'register.html')