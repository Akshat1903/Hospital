from django.shortcuts import render,redirect,get_object_or_404
from .forms import (UserForm,
                    DoctorProfileForm,
                    UserUpdateForm,
                    DoctorProfileUpdateForm,
                    PatientForm)
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import DoctorProfile,Patient
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.contrib import messages
from bootstrap_datepicker_plus import DatePickerInput

def homepage(request):
    return render(request,'accounts/homepage.html')

def index(request):
    return render(request,'accounts/index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'accounts/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logged Out successfully")
    return redirect('index')


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = DoctorProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            profile.save()
            messages.success(request, "Registered Successfully! Please login now")
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = DoctorProfileForm()
    return render(request,'accounts/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

@login_required
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'accounts/profile.html', args)

@login_required
def edit_profile(request, pk):
    try:
        profile = request.user.doctorprofile
    except DoctorProfile.DoesNotExist:
        profile = DoctorProfile(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = DoctorProfileUpdateForm(request.POST,instance=profile)
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            profile_1 = profile_form.save(commit=False)
            if 'image' in request.FILES:
                profile_1.image = request.FILES['image']
            profile_1.save()
            messages.success(request, "Profile updated successfully")
            return redirect('index')
        else:
            print(user_form.errors,profile_form.errors)
    else:
        instance_user = User.objects.get(pk=pk)
        user_form = UserUpdateForm(request.POST or None, instance=instance_user)
        profile_form = DoctorProfileUpdateForm(request.POST or None, instance=profile)

    return render(request, 'accounts/edit.html', {'user_form': user_form,
                                                    'profile_form':profile_form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST , user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password changed")
            return redirect('index')
        else:
            return redirect('accounts:change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request,'accounts/change_password.html',args)

@login_required
def patient_list(request):
    query = request.GET.get("q", None)
    qs = Patient.objects.filter(doctor=request.user)
    if query is not None:
        qs = qs.filter(
                Q(name__icontains=query) |
                Q(case__icontains=query)
                )
    context = {
        "object_list": qs,
    }
    template = "accounts/patientlist.html"
    return render(request, template, context)

@login_required
def patient_detail(request, id=None):
    obj = get_object_or_404(Patient, id=id)
    context = {
        "object": obj,
    }
    template = "accounts/patientdetail.html"
    return render(request, template, context)

@login_required
def patient_create(request):
    form = PatientForm(request.POST or None)
    form.fields['dob'].widget = DatePickerInput()
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.doctor = request.user
        if 'report' in request.FILES:
            obj.report = request.FILES['report']
        obj.save()
        messages.success(request, "Added a new Patient {}".format(obj.name))
        context = {
            "form": PatientForm()
        }
        return redirect('accounts:patient_list')

    template = "accounts/createpatient.html"
    return render(request, template, context)

@login_required
def patient_delete(request, id=None):
    obj = get_object_or_404(Patient, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Patient Removed")
        return redirect('accounts:patient_list')
    context = {
        "object": obj,
    }
    template = "accounts/deletepatient.html"
    return render(request, template, context)

@login_required
def patient_update(request, id=None):
    obj = get_object_or_404(Patient, id=id)
    form = PatientForm(request.POST or None, instance=obj)
    form.fields['dob'].widget = DatePickerInput()
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        if 'report' in request.FILES:
            obj.report = request.FILES['report']
        obj.save()
        messages.success(request, "Updated Patient {}".format(obj.name))
        return redirect('accounts:patient_list')
    template = "accounts/updatepatient.html"
    return render(request, template, context)
