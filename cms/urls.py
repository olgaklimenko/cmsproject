from django.conf.urls import patterns, url
from cms.models import Story
from cms import views

urlpatterns = patterns('',
    url(r'^category/(?P<slug>[-\w]+)/$', views.category, name='cms-category'),
    url(r'^search/$', views.search, name='cms-search'),
    url(r'^(?P<slug>[-\w]+)/$', views.StoryDetail.as_view(), name='cms-story'),
    url(r'^$',  views.CategoryList.as_view(), name='cms-home'),
)
