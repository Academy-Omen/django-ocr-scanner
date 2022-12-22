from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import ocr_image, ocr_test

# 
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ocr_image, name='ocr_image'),
    path('ocr_test/', ocr_test, name='ocr_image'),
    # serve media files
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    # setting this to view media files from admin panel
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
