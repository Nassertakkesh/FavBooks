from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^addingbook$', views.addingbook),
    # url(r'^thewall$', views.thewall),
    # url(r'^delete$', views.delete),
    url(r'^book$', views.presuccess),
    url(r'^eidtbook/(?P<id>\d+)$', views.editbook),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^book/(?P<id>\d+)$', views.books_page),
    url(r'^favorite/(?P<id>\d+)$', views.favorite),
    url(r'^book/unfavorite/(?P<id>\d+)$', views.unfavorite),
    url(r'^book/favorite/(?P<id>\d+)$', views.favorite),
    url(r'^fav_books$', views.fav_books),

    # url(r'^comment$', views.comment),

]