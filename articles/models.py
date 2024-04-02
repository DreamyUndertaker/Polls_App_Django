from django.db import models


class Lecture(models.Model):
    title = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='lectures/pdfs/')

    def str(self):
        return self.title

    class Meta:
        verbose_name = 'Файл лекций'
        verbose_name_plural = 'Файлы лекций'
