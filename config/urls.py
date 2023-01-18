from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('index/honyaku/archive/admin/', admin.site.urls),
    path('index/honyaku/archive/accounts/', include('django.contrib.auth.urls')),
    path('index/honyaku/archive/', include('resources.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
