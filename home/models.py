from django.db import models
from django.urls import reverse


class Instructions(models.Model):
    title = models.CharField(max_length=30)
    file = models.FileField(upload_to='instructions/', default=None, null=False, blank=False)

    def get_absolute_url(self):
        return reverse("instruction_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Инструкции"
        verbose_name = "Инструкцию"
