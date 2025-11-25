"""
URL coreuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import views, settings

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.permissions import AllowAny


from users import views as user_views
from transactions import views as transation_views

schema_view = get_schema_view(
      openapi.Info(
      title="My API",
      default_version='v1',
      description="My API description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[AllowAny],
)


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('signup/', user_views.signup, name='signup'),


    path("transactions/", include('transactions.urls')),
    path("accounts/", include("accounts.urls")),
    path("users/", include("users.urls")),
    path("analysis/", include("analysis.urls")),



    # swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)