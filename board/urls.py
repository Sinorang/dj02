from django.urls import path
from . import views

app_name = "board"
urlpatterns = [
    path('index/', views.index, name="index"),
    path('detail/<bpk>', views.detail, name="detail"),
    path('create/', views.create, name="create"),
    path('delete/<bpk>', views.delete, name="delete"),
    path('update/<bpk>', views.update, name="update"),
    path('likey/<bpk>', views.likey, name="likey"),
    path('unlikey/<bpk>', views.unlikey, name="unlikey"),
    path('creply/<bpk>', views.creply, name="creply"),
    path('dreply/<bpk>/<rpk>', views.dreply, name="dreply")
]