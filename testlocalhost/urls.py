"""testlocalhost URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'blog.views.index',name="index"),
    url(r'^login/$', 'blog.views.login',name="login"),
    url(r'^logout/$', 'blog.views.logout',name="logout"),
    url(r'^register/$', 'blog.views.registerPage',name="registerPage"),
    url(r'^doregister/$', 'blog.views.register',name="doregister"),
    url(r'^admin/$', 'blog.views.dashbord',name="dashbord"),
    url(r'^usermanage/$', 'blog.views.usermanage',name="usermanage"),
    url(r'^add_question/$', 'blog.views.addQuestion',name="add_question"),
    url(r'^my_question/$', 'blog.views.myQuestion',name="my_question"),
    url(r'^my_account/$', 'blog.views.myAccount',name="my_account"),
    url(r'^do_add_question/$','blog.views.do_addQuestion',name="do_add_question"),
    url(r'^do_upload/$','blog.views.do_upload',name="do_upload"),
    url(r'^do_imgreplace/$','blog.views.do_imgreplace',name="do_imgreplace"),
    url(r'^do_access/$','blog.views.do_access',name="do_access"),
    url(r'^do_deny/$','blog.views.do_deny',name="do_deny")

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
