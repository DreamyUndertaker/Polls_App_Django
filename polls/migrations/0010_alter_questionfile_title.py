# Generated by Django 4.2.5 on 2024-04-08 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_alter_answer_options_alter_question_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionfile',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]