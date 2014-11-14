from django.shortcuts import render
from django.http import HttpResponse

from .forms import CategoryForm, PageForm
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
