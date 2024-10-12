"""
URL configuration for task_scheduler project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from rest_framework import routers
from scheduler.views import (
    LoginView,
    LogoutView,
    TaskViewSet,
    UserListViewSet,
    UserRegistrationViewSet,
)

router = routers.DefaultRouter()
router.register(r"register", UserRegistrationViewSet, basename="user-registration")
router.register(r"users", UserListViewSet, basename="user-list")
router.register(r"tasks", TaskViewSet, basename="task")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
