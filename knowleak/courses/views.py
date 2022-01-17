from django.shortcuts import render, get_object_or_404
from . models import Course, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import User
from django.shortcuts import redirect
import datetime

def course_list(request, category_slug=None):
    category_page = None
    categories = Category.objects.all()
    current_user = request.user

    if category_slug != None:
        category_page = get_object_or_404(Category, slug=category_slug)
        courses = Course.objects.filter(available=True, category= category_page)

    else:
        courses = Course.objects.all().order_by('-year', 'month', 'day')

    page = request.GET.get('page', 1)
    paginator = Paginator(courses, 2)

    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    if current_user.is_authenticated:
        enrolled_courses = current_user.courses_joined.all()
    else:
        enrolled_courses = courses

    
    context = {
        'courses': courses,
        'enrolled_courses': enrolled_courses,
        'user' : current_user,
        'categories': categories,
        
    }

    return render(request, 'courses.html', context)



def course_detail(request, category_slug, course_id):
    current_user = request.user
    course = Course.objects.get(category__slug=category_slug, id = course_id)
    courses = Course.objects.all()
    categories = categories = Category.objects.all()
    token = course.token
    user_token = current_user.token
    student_count = course.students.count()
    
    if student_count != 0:
        coin_willbepaid = token/student_count
    else:
        coin_willbepaid = token
    can_enrolled = False

    if user_token>=coin_willbepaid:
        can_enrolled = True
    

    if current_user.is_authenticated:
        enrolled_courses = current_user.courses_joined.all()

    else:
        enrolled_courses = courses

    #enrolled_courses = current_user.courses_joined.all()
    context = {
        'course': course,
        'enrolled_courses': enrolled_courses,
        'categories': categories,
        'user' : current_user,
        'can_enrolled' : can_enrolled,
        'coin_willbepaid' : coin_willbepaid
    }
    return render(request, 'course.html', context)

def search(request):
    
    courses = Course.objects.filter(name__contains = request.GET['search'])
    categories = Category.objects.all()

    context = {
        'courses': courses,
        'categories': categories,
    }
    return render(request, 'courses.html', context)

def add_course(request):
    teachers = User.objects.filter(is_teacher=True)
    categories = Category.objects.all()

    context = {
        'teachers' : teachers,
        'categories' : categories,
    }


    return render(request, 'add_course.html', context)

def add(request):
   
    name = request.POST.get("name")
    teacher = request.user.get_username()
    category = request.POST.get("category")
    description = request.POST.get("description")
    token = request.POST.get("token")


    print(name, teacher, category, description, date,appt, token)
    return redirect("/courses/add_course/")
"""
    if(name != None and date != ""):
        o_ref = Course(name=name, teacher=teacher,  description = description, date = date)
        o_ref.save()
    else:
        print("no")"""
   

def add_category(request):
    
    name = request.POST.get("name")
    slug = request.POST.get("slug")
    print(name, slug)
    
    if(name != None and slug != None):
        o_ref = Category(name=name, slug=slug.lower())
        o_ref.save()
    
    return redirect("/courses/add_course/")
