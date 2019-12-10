from django.urls import path
from logic import views

urlpatterns = [
    path('', views.index, name='landing'),
    path('index/', views.index, name='index'),
    path('create_game/', views.create_game_service, name='create_game'),
    path('join_game/', views.join_game_service, name='join_game'),
    path('select_game/', views.select_game_service, name='select_game'),
    path('select_game/<int:game_id>/', views.select_game_service, name='select_game'),
    path('signup/', views.signup_service, name='signup'),
    path('login/', views.login_service, name='login'),
    path('logout/', views.logout_service, name='logout'),
    path('move/', views.move_service, name='move'),
    path('move/', views.move_service, name='move'),
    path('play/', views.show_game_service, name='show_game'),
    path('counter/', views.counter_service, name='counter'),
]
