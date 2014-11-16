from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
from .models import Category, Page

def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories':category_list, 'pages':page_list}

    return render(request, 'rango/index.html', context_dict)

def category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name or category_name_slug
        context_dict['category'] = category
        context_dict['category_name_slug'] = category_name_slug

        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages

    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form':form})

@login_required
def add_page(request, category_name_slug):
    cate = None
    context_dict = {}
    try:
        cate = Category.objects.get(slug=category_name_slug)
        if request.method == 'POST':
            form = PageForm(request.POST)

            if form.is_valid():
                page = form.save(commit=False)
                page.category = cate
                page.views = 0
                page.save()
                return category(request, category_name_slug)
            else:
                print form.errors

        else:
            form = PageForm()
        context_dict.update({'form':form, 'category':cate})

    except Category.DoesNotExist:
        pass

    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse('Your rango account is disabled')
        else:
            print 'Invalid login details: %s, %s' % (username, password)
            return HttpResponse('Invalid login details provided!')
    else:
        return render(request, 'rango/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

