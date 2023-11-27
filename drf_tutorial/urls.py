from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework.authtoken.views import obtain_auth_token
from my_api import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('my_api/', include(urls)),
    path('auth/', obtain_auth_token)
]
