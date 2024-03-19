from django.urls import include, path
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('home/', include('home.urls')),
]
