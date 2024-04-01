# Generated by Django 3.2.25 on 2024-03-28 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_usertest_question_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertest',
            name='is_correct',
        ),
        migrations.AddField(
            model_name='usertest',
            name='correct_answers_count',
            field=models.IntegerField(default=0),
        ),
    ]