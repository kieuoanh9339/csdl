from django.urls import path
from django.urls.conf import include
from thuvien import views
from thuvien.api import urls as api_urls

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('api/', include(api_urls)),
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('history/', views.history, name='history'),
    path('account/', views.account, name='account'),
    path('timkiem/', views.search, name='search'),
]