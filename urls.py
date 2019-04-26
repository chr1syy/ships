from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('<int:shipid>/', views.detail, name='detail'),
	path('list/<int:groupid>/', views.list, name='list'),
	path('<int:shipid>/ajax/spawn/', views.ajax_spawn, name='ajax_spawn'),
]
