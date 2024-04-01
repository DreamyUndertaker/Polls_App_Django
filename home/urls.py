from django.urls import include, path

from .views import HomeView, InstructionDetail

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('<int:pk>', InstructionDetail.as_view(), name="instruction_detail"),
    path('documents/', include('articles.urls')),
    path('polls/', include('polls.urls')),

]
