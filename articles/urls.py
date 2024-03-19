from django.urls import path

from .views import DocumentsView


urlpatterns = [
    path('', DocumentsView.as_view(), name='documents')
]
