from django.urls import path

from . import views

app_name = "cube_solver_app"

urlpatterns = [
    path('', views.index, name="index"),
    path('solve/', views.solve, name="solve")
]