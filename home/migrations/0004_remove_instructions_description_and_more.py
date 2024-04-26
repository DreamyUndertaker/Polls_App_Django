# Generated by Django 4.2.5 on 2024-04-01 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_instructions_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructions',
            name='description',
        ),
        migrations.AlterField(
            model_name='instructions',
            name='file',
            field=models.FileField(default=None, upload_to='home/instructions/'),
        ),
    ]