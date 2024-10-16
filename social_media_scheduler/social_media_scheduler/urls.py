from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('publicacao/', include('publicacao.urls')),
    path('banco/', include('publicacao_bau.urls')),
    path('perfil/', include('perfil.urls')),
    path('logout/', LogoutView.as_view(next_page='/user/login'), name='logout'),
    path('', RedirectView.as_view(url='/user/login')),
    path('webservice/', include('webservice.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
