from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, UserProfileForm, Vacancy,Applications,Query
from django.contrib.auth.models import User
from .models import UserProfile, vacancy, DeptProfile, applications,query,notifications
from django.core.files.storage import FileSystemStorage

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            user.username = email.split('@')[0]
            # password = id_generator()
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'sih/base.html', )
    else:
        form = UserForm()

    return render(request, 'sih/signup.html', {'form': form})

def logout(request):
    logout(request)

    return render(request, 'sih/base.html')

def index(request):
    dept_result = None
    vacancy_result  = None
    all = True
    if request.method=="POST":
        search = request.POST.get('search')
        dept_result = DeptProfile.objects.filter(dept_name=search)
        vacancy_result = vacancy.objects.filter(title=vacancy_result)
        all = False

    else:
        dept_result = DeptProfile.objects.filter()
        vacancy_result = vacancy.objects.filter()
        
    return render(request, 'sih/base.html',{'dept_result':dept_result,'vacancy_result':vacancy_result,'all':all})

def profile(request):
    form = None
    Elementry = 'Elementry'
    HighSchool =  'High School'
    SeniorSecondary = 'Secondary Education'
    Undergraduate = 'Undergraduate'
    Postgraduate = 'Postgraduate'
    Doctorate = 'Doctoral Degree'

    QUALIFICATIONS = (
        (Elementry, Elementry),
        (HighSchool,  HighSchool),
        (SeniorSecondary, SeniorSecondary),
        (Undergraduate, Undergraduate),
        (Postgraduate, Postgraduate),
        (Doctorate, Doctorate),
    )

    Male = 'Male'
    Female =  'Female'
    Others = 'Others'
    
    GENDER = (
        (Male, Male),
        (Female,  Female),
        (Others, Others),
    )
    if request.user.is_authenticated:
        if request.method=="POST":
            form = UserProfileForm(request.POST)
            if form.is_valid():
                print (1)
                age = form.cleaned_data['age']
                gender = request.POST.get('gender')
                qualification = request.POST.get('qualification')
                resume = request.FILES['resume']
                profilepicture = request.FILES['profilepicture']
                fs = FileSystemStorage()
                filename_resume = fs.save(resume.name, resume)
                uploaded_resume_url = fs.url(filename_resume)

                filename_profilepicture = fs.save(profilepicture.name, profilepicture)
                uploaded_profilepicture_url = fs.url(filename_profilepicture)

                if request.POST.get('is_subscribed')=="True":
                    is_subscribed = True
                user = User.objects.get(username=request.user.username)

                Profile = UserProfile.objects.create(user=user,age=age,gender=gender,resume=resume,profilepicture=profilepicture,is_subscribed=is_subscribed,qualification=qualification)
                Profile.save()

                return render(request, 'sih/profile.html', {
                    'uploaded_resume_url': uploaded_resume_url,
                    'uploaded_profilepicture_url': uploaded_profilepicture_url,
                    'qualifications_choices':QUALIFICATIONS,
                    'age_choices':GENDER
                })

        else:
            form = UserProfileForm()

        return render(request, 'sih/profile.html', {'form': form, 'status':'logged_in','qualifications_choices':QUALIFICATIONS,'age_choices':GENDER})

    else:
        return redirect('sih:signup')

def vacancies(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form = Vacancy(request.POST)
            if form.is_valid():
                title = request.POST.get('title')
                description = request.POST.get('description')
                num_slots = int(request.POST.get('num_slots'))
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                if request.POST.get('results_out')=="True":
                    results_out = True
                dept_user = DeptProfile.objects.get(user=request.user)
                New_vacancy = vacancy.objects.create(title=title,description=description,num_slots=num_slots,start_date=start_date,end_date=end_date,results_out=results_out,dept_id=dept_user)
                New_vacancy.save()
        else:
            form = Vacancy()
            
        return render(request, 'sih/vacancies.html', {'form': form, 'status':'logged_in'})

    else:
        return redirect('sih:signup')

def query(request):
    if request.user.is_authenticated:
        pass

    else:
        return redirect('sih:signup')

def applications(request):
    if request.user.is_authenticated:
        pass

    else:
        return redirect('sih:signup')



