from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_questions, name='upload_questions'),
    path('', views.test_list, name='test_list'),
    path('test/<int:test_id>/', views.test_detail, name='test_detail'),
    path('submit_test/<int:question_file_id>/', views.submit_test, name='submit_test'),
]
