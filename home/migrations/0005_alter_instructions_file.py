# Generated by Django 4.2.5 on 2024-04-08 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_instructions_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructions',
            name='file',
            field=models.FileField(default=None, upload_to='instructions/'),
        ),
    ]
