from django.urls import path
from test import settings
from articles import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.LecturesList.as_view(), name='lecture_list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

