from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:number>", views.details, name="details")
]