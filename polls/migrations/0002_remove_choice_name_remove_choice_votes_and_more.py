# Generated by Django 4.2.5 on 2024-03-22 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='name',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='votes',
        ),
        migrations.RemoveField(
            model_name='question',
            name='name',
        ),
        migrations.RemoveField(
            model_name='question',
            name='published',
        ),
        migrations.AddField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='choice',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='question_text',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
