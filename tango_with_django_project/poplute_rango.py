# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page


def add_cate(name, views=0, likes=0):
    c, created = Category.objects.get_or_create(name=name)
    c.views = views
    c.likes = likes
    c.save()
    return c

def add_page(cate, title, url, views=0):
    p = Page.objects.get_or_create(title=title, url=url, views=views, category=cate)[0]
    return p

def populate():

    python_cate = add_cate('Python', views=128, likes=64)

    add_page(cate=python_cate, title='Official Python Tutorial',
             url="http://docs.python.org/2/tutorial/",
             views=4)

    add_page(cate=python_cate, title="How to think like a computer scientist",
             url="http://www.greenteapress.com/thinkpython",
             views=10)

    add_page(cate=python_cate, title="Learn Python in 10 Minutes",
             url="http://www.korokithakis.net/tutorials/python/",
             views=18)

    django_cate = add_cate('Django', views=64, likes=32)

    add_page(cate=django_cate, title="Official Django Tutorial",
             url="https://docs.djangoproject.com/en/1.7/intro/tutorial01/",
             views=43)

    add_page(cate=django_cate, title="Django Rock",
             url="http://www.djangorocks.com/",
             views=11)

    add_page(cate=django_cate, title="How to tango with Django",
             url="http://www.tangowithdjango.com/",
             views=54)

    framework_cate = add_cate('Other Frameworks', views=32, likes=16    )

    add_page(cate=framework_cate, title="Bottle",
             url="http://bootlepy.org/docs/dev/",
             views=77)

    add_page(cate=framework_cate, title='Flask',
             url="http://flask.pocoo.org",
             views=83)

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print '- %s - %s' %(str(c), str(p))


if __name__ == '__main__':
    print 'starting rango population script...... gooooo'
    populate()