from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.
def employee(request):
    if request.method == "POST":
        employee_name = request.POST.get('employee_name')
        employee_position = request.POST.get('employee_position')

        query = Employee.objects.all().filter(employee_comp_name="repliq")
        Employee.objects.create(
            employee_id = len(query)+1,
            employee_name = employee_name,
            employee_position = employee_position,
            employee_comp_name = "repliq",
        )

        return redirect('/')

    queryset = Employee.objects.all()
    context = {'employees' : queryset}

    return render(request, 'employee.html', context)

def device(request):
    if request.method == "POST":
        device_model = request.POST.get('device_model')
        device_type = request.POST.get('device_type')
        device_condition = request.POST.get('device_condition')

        
        query = Device.objects.all().filter(device_comp_name="repliq")
        Device.objects.create(
            device_id = len(query)+1,
            device_model = device_model,
            device_type = device_type,
            device_condition = device_condition,
            device_comp_name = "repliq",
        )

        return redirect('/device/')

    queryset = Device.objects.all()
    context = {'devices' : queryset}

    return render(request, 'device.html', context)


def check_out(request, id):
    if request.method == "POST":
        _condition = request.POST.get('_condition')
        _employee_id = request.POST.get('_employee_id')

        print(_condition)
        print(_employee_id)
        
        queryset = Device.objects.get(id = id)
        queryset.device_occupied_by = int(_employee_id)
        queryset.save()

        print(queryset.device_condition)
        DeviceLogInfo.objects.create(
            device_id = queryset.device_id,
            device_comp_name = queryset.device_comp_name,
            device_occupied_by = int(_employee_id),
            device_checkout_time = timezone.now(),
            device_checkout_condition = _condition,
        )
        return redirect('/device')
    return render(request, 'checkoutform.html')

def return_back(request, id):
    if request.method == "POST":
        _condition = request.POST.get('_condition')
        queryset = Device.objects.get(id = id)
        queryset.device_occupied_by = 0
        queryset.save()

        #update devicesLogInfo table
        log_queryset = DeviceLogInfo.objects.all().filter(device_id = queryset.device_id).latest('id')
        print(log_queryset)
        log_queryset.device_return_back_time = timezone.now()
        log_queryset.device_return_back_condition = _condition
        log_queryset.save()

        print(queryset.device_condition)
        return redirect('/device/')
    return render(request, 'returnform.html')


#viewing devices log history
def device_log(request):
    queryset = DeviceLogInfo.objects.all()
    context = {'devices' : queryset}
    return render(request, 'devicelog.html', context)