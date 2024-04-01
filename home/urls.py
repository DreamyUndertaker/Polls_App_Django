from django.conf.urls.static import static
from django.urls import include, path

from test import settings
from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('documents/', include('articles.urls')),
    path('polls/', include('polls.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
