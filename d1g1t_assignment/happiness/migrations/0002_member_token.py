# Generated by Django 4.0.4 on 2022-04-22 02:01

from django.db import migrations, models
import happiness.models


class Migration(migrations.Migration):

    dependencies = [
        ('happiness', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='token',
            field=models.CharField(default=happiness.models.auth_token_generator, max_length=32),
        ),
    ]
