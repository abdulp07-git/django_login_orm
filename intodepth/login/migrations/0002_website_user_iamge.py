# Generated by Django 5.0.7 on 2024-07-10 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='website_user',
            name='iamge',
            field=models.ImageField(default=0, upload_to='pics'),
            preserve_default=False,
        ),
    ]
