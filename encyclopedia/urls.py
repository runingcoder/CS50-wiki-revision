from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path for each entry
    path("wiki/<str:entry>", views.entry, name='entry'),
        path('search/', views.search, name='search'),
    path('create/', views.create, name='create'),
    path('edit/<str:entry>', views.edit, name="edit"),

]
