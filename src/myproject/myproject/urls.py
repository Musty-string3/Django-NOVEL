from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('text_app/', include('text_app.urls')),
    path('accounts/', include('allauth.urls')),
]
