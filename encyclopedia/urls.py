from django.urls import path
from . import views


app_name = 'encyclopedia'


urlpatterns = [
    path("", views.index, name="index"),
    path('<str:title>/', views.page, name='page'),
    path('search', views.search, name='search'),
    path('create', views.createPage, name='createPage'),
    path('edit/<str:title>', views.edit, name='edit'),
    path('random', views.random, name='random')
]
