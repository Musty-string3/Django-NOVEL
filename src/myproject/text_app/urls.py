from django.urls import path
from . import views

app_name = 'text_app'
urlpatterns = [
    path('novels/', views.IndexNovel.as_view(), name='novel_index'),
]
