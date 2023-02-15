from django.urls import path
from . import views

urlpatterns = [
    path('sach/', views.SachRoute.as_view()),
    path('sach/<int:id>', views.SachByIdRoute.as_view()),
    path('auth/login/', views.LoginRoute.as_view()),
    path('auth/register/', views.SignUpRoute.as_view()),
    path('themuon/', views.TheMuonRoute.as_view()),
    path('me/', views.NguoiMuonRoute.as_view()),
]

