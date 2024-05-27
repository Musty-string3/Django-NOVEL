from django.urls import path
from . import views

app_name = 'text_app'
urlpatterns = [
    path('novels/', views.IndexNovelView.as_view(), name='index_novel'),
    path('novel/<int:pk>', views.DetailNovelView.as_view(), name='detail_novel'),
    path('novel/create/', views.CreateNovelView.as_view(), name='create_novel'),
]