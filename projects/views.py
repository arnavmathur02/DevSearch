from django.shortcuts import redirect, render

from .models import Project
from .forms import ProjectForm

from django.contrib.auth.decorators import login_required


# Create your views here

def projects(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    #tags = Project.tags.all()
    return render(request, 'projects/single-project.html', {'project' : projectObj})


## this decorator requires "user" to be logged in. 
## if in case, he's not logged in then he gets redirected to 'login' page
@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        ## request.FILES is used when the form will also send in files like images, doc, etc
        form = ProjectForm(request.POST, request.FILES) 
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project-form.html', context)



@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile

    ## Here we get all the project with the id but checking all data(prpjects)
    #project = Project.objects.get(id=pk)

    ##### ANOTHER WAY
    ## Here we are querying the projects of only the logged in user.
    project = profile.project_set.get(id=pk)

    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project-form.html', context)



@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile

    ### Doing the same thing as in update method
    #project = Project.objects.get(id=pk)

    project = profile.project_set.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    context = {'object': project}
    return render(request, 'delete-template.html', context)