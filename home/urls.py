from django.urls import include, path

from .views import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('documents/', include('articles.urls')),
    path('polls/', include('polls.urls')),

]
