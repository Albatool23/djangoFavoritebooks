from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('signout', views.signout),
    path('addBook', views.addBook),
    path('displybook/<ID>', views.displybook),
    path('edit', views.edit),
    path('Favorite/<ID>', views.Favorite),
    path('unFavorite/<ID>', views.unFavorite),

]