from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),

    # Main API routes from the 'api' app
    path('api/', include('api.urls')),

    # Token authentication endpoint
    # Users POST their username and password here to receive an auth token
    path('api/token/', obtain_auth_token, name='api_token'),
]
