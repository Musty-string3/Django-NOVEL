from django.contrib import admin
from django.urls import path, include
from .views import TopView

urlpatterns = [
    path('', TopView.as_view(), name='top'),
    path('admin/', admin.site.urls),
    path('text_app/', include('text_app.urls')),
    path('accounts/', include('allauth.urls')),
]
