# Generated by Django 3.2.25 on 2024-03-27 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.questionfile'),
        ),
        migrations.AlterField(
            model_name='questionfile',
            name='file',
            field=models.FileField(default=None, upload_to='polls/quiz/'),
        ),
        migrations.AlterField(
            model_name='questionfile',
            name='title',
            field=models.CharField(default='1', max_length=255),
        ),
    ]
