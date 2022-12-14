from django.shortcuts import render, redirect
from django.urls import is_valid_path
from .models import Profile, Skill

from django.contrib.auth.models import User

from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def loginUser(request):
    page = 'login'

    ## if user is already logged in, no need to send him to login page. Hence always redirect him to profiles page
    if request.user.is_authenticated:
        return redirect('profiles')


    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            ## Checking if the user exists in our "User" table
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist!')

        ## authenticate method checks the username and password against the User instance queried above
        ## authenticate either returns a "user" or "None"
        user = authenticate(request, username=username, password=password)

        if user is not None:
            ## login() creates a user in the sessions table created automatically by django
            ## then login() adds the user into browsers cookies
            login(request, user)
            return redirect('profiles')

        else:
            messages.error(request, 'username or password is incorrect!')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    ## logout() method deletes the current user from the session
    ## also deletes from the browser's cookies
    logout(request)
    messages.success(request, 'user was logged out!')
    return redirect('login')


def registerUser(request):
    page = 'register'

    form = CustomUserCreationForm()

    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created succesfully!')

            login(request, user)
            return redirect('edit-account')

        else:
            messages.error(request, 'An error has occured!')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact = "")
    otherSkills = profile.skill_set.filter(description = "")

    context = {
        'profile': profile,
        'topSkills' : topSkills,
        'otherSkills': otherSkills
    }
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    
    context = {'profile': profile, 'skills' : skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)



@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method =='POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added succesfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method =='POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated succesfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted succesfully!')
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete-template.html', context)