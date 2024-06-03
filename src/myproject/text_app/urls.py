from django.urls import path
from . import views

app_name = 'text_app'
urlpatterns = [
    path('novels/', views.NovelIndexView.as_view(), name='index_novel'),
    path('novel/<int:pk>', views.NovelDetailView.as_view(), name='detail_novel'),
    path('novel/new/', views.NovelNewView.as_view(), name='new_novel'),
    path('novel/<int:pk>/edit', views.NovelEditView.as_view(), name='edit_novel'),
    path('novel/<int:pk>/delete', views.NovelDeleteView.as_view(), name='delete_novel'),

    path('characters/', views.CharacterIndexView.as_view(), name='index_character'),
    path('characters/new', views.CharacterNewView.as_view(), name='new_character'),
    path('character/<int:pk>/edit', views.CharacterEditView.as_view(), name='edit_character'),
    path('character/<int:pk>/delete', views.CharacterDeleteView.as_view(), name='delete_character'),
]