from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name="login"),
    path('login/', views.login_view, name="login"),
    path('home/', views.home_view, name="home"),
    path('get_features/<int:folder_id>/', views.get_features, name='get_features'),
    path('get_sublayers/<str:feature_title>/', views.get_sublayers, name='get_sublayers'),
    path('download/<str:feature_title>/<str:sublayer>/<str:filetype>/', views.download, name='download'),
    path('download/<str:feature_title>/<str:filetype>/',views.download_webmap, name = 'download_webmap'),
    path('clear/', views.clear, name='clear'),
]