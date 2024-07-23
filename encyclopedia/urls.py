from django.urls import path
from . import views


app_name = 'encyclopedia'


urlpatterns = [
    path("wiki/", views.index, name="index"),
    path('wiki/<str:title>/', views.page, name='page'),
    path('wiki/search', views.search, name='search'),
    path('wiki/create', views.createPage, name='createPage'),
    path('wiki/edit/<str:title>', views.edit, name='edit'),
    path('wiki/random', views.random, name='random')
]
