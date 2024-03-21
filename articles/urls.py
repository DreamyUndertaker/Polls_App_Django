from django.urls import path
from test import settings
from articles import views
from django.conf.urls.static import static

urlpatterns = [
    path('upload', views.model_form_upload,  name='documents'),
    path('', views.documentsList, name='list')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

