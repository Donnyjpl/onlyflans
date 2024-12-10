from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # App Web
    path("web/", include('web.urls')),
    # Usuarios
     path('carrito/', include('compra.urls')),
    path('compra/', include('compra.urls')),
    path("accounts/", include('django.contrib.auth.urls')),
]

