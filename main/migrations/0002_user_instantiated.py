# Generated by Django 4.0.4 on 2023-02-09 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='instantiated',
            field=models.BooleanField(default=False),
        ),
    ]
