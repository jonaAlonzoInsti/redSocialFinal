from django.contrib import admin
from django.urls import path, include
from .views import HomeView, LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('allauth.urls')),  # Corrección aquí
    path('users/', include('accounts.urls', namespace='users')),
    #editar, ver, eliminar post
    path('social/', include('social.urls', namespace='social')),
    #deslogeo de usuario
    path('logout/', LogoutView.as_view(), name='logout'),


    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
