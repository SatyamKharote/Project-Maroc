# Generated by Django 4.1.5 on 2023-01-27 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_profile_forgot_password_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]
