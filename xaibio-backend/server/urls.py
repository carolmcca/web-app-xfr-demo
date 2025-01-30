"""
URL configuration for drinks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from server import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/', include([path('admin/', admin.site.urls),
        path('healthcheck/', views.health_check, name='health_check'),
        
        path('images/', views.get_image, name='get_image'),
        path('images/verify/', views.verify_images, name='verify_images'),
        path('images/identify/', views.identify_image, name='identify_image'),
        path('images/examples/', views.example_images, name='example_images'),

        path('users/images/', views.users_get_or_add_images, name='users_get_or_add_images'),
        path('users/verify/', views.verify_user, name='verify_user'),
        path('users/images/delete/', views.users_delete_image, name='users_delete_image'),
        path('users/register/', views.users_register, name='users_register'),
        path('users/auth/', views.users_auth, name='users_auth'),
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('users/', views.users_delete, name='users_delete'),
    
        path('delete_all_images/', views.delete_all_images, name='delete_all_images'),
        path('add_dummy_images/', views.add_dummy_images, name='add_dummy_images'),
    ])
        )
]

urlpatterns = format_suffix_patterns(urlpatterns) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
