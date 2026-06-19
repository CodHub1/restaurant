"""Главный URL-конфигуратор проекта."""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = 'Администрирование сайта «Старик и море»'
admin.site.site_title = 'Старик и море — админ-панель'
admin.site.index_title = 'Управление контентом ресторана'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
