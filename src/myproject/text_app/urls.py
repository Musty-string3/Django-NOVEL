from django.urls import path
from . import views

app_name = 'text_app'
urlpatterns = [
    path('novels/', views.NovelIndexView.as_view(), name='index_novel'),
    path('novel/<int:pk>', views.NovelDetailView.as_view(), name='detail_novel'),
    path('novel/new/', views.NovelNewView.as_view(), name='new_novel'),
    path('novel/edit/<int:pk>', views.NovelEditView.as_view(), name='edit_novel'),
    path('novel/delete/<int:pk>', views.NovelDeleteView.as_view(), name='delete_novel'),
]