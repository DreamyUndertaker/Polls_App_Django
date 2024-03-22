from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_questions, name='upload_questions'),
    path('display/', views.display_questions, name='display_questions'),
    path('take-test/', views.take_test, name='take_test'),
    path('test-result/', views.test_result, name='test_result'),
]
