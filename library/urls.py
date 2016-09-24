__author__ = 'ahmedzouari'
from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^checkouts/$', views.checkouts, name='checkouts'),
    url(r'^checkin/$', views.checkin, name='checkin'),
    url(r'^add_borrower/$', views.add_borrower, name='add_borrower'),
    url(r'^fines/$', views.fines, name='fines'),
    url(r'^listfines/$', views.listfines, name='listfines'),
    url(r'^payfines/$', views.payfines, name='payfines'),
]