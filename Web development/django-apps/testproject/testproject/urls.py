"""testproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(
        "", include("dashboard.urls")
    ),  # ----redirect the request to urls.py of dashboard app
    path("admin/", admin.site.urls),  # -----redirect the request to admin site app
    path(
        "api/", include("api.urls")
    ),  # ------redirect the request to urls.py of api app
    path(
        "api_noauth/", include("api_noauth.urls")
    ),  # -------redirect the request to urls.py of api_noauth app
]
