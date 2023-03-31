"""Project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from orders.views import BookViewSet, index_1, auth, UserBookRelationViewSet, UserViewSet

router = SimpleRouter()
router.register(r'books', BookViewSet)
router.register(r'relation', UserBookRelationViewSet)
router.register(r'users',UserViewSet)

urlpatterns = [
    re_path('', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('', index_1),
    path('auth/', auth),
    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += router.urls  # добавляем юрлы роутера
