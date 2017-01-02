"""djangoAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from books.views import hello 
from books.views import hello2
from books.views import search
from books.views import search2
from books.views import CSV2
from books.views import SaveProfile
from books.views import join
from django.views.generic import RedirectView
from books.views import index
from simpleticket.views import predict#WebService##
from simpleticket.views import post1 #predict#
#from simpleticket.views import create
#from django.views.generic import TemplateView
#from books.views import PublisherList
#from books.views import AuthorDetailView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello/$', hello),
    url(r'^hello2/$', hello2),
    url(r'^search1/$', search),
    url(r'^search2/$', search2),
    url(r'^csv/$', CSV2),
    url(r'^profile/$',SaveProfile),
    url(r'^join/$', join),
    url(r'^post/$', predict),
    url(r'^poc/$', index),
    #url(r'^tickets/', include('simpleticket.urls')),
    url(r'^predict/$', post1),
    #url(r'^about/$',WebService.as_view()),
    #TemplateView.as_view(template_name = 'profile.html')), 
      #url(r'^saved/', 'SaveProfile', name = 'saved'),
   # url(r'^publishers/$', PublisherList.as_view()),
   # url(r'^authors/(?P<pk>[0-9]+)/$', AuthorDetailView.as_view(), name='author-detail\
#'),
]
