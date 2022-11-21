from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('members/', views.members, name='members'),
    path('payments/', views.payment, name='payments'),
    path('timetables/', views.timetable, name='titmetables'),
    path('meetings/', views.meeting, name='meetings'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('profile/', views.profile, name='user-profile'),
    path('member/<str:pk>/', views.member, name='member_detail'),
]