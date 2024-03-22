# Generated by Django 4.2.5 on 2024-03-22 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('pdf_file', models.FileField(upload_to='lectures/pdfs/')),
            ],
        ),
        migrations.DeleteModel(
            name='Document',
        ),
    ]