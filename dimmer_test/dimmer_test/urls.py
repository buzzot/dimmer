from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin (optional)
    path('', include('dimmer_matching.urls')),  # Root URL to your app's URLs
]
