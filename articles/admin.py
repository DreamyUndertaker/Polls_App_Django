from django.contrib import admin
from .models import Document

class Documnet(admin.TabularInline):
    model = Document

admin.site.register(Document)