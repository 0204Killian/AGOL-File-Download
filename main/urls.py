from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name="login"),
    path('login/', views.login_view, name="login"),
    path('home/', views.home_view, name="home"),
    path('get_features/<int:folder_id>/', views.get_features, name='get_features'),
]