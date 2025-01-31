# Generated by Django 5.0.7 on 2024-07-10 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_rename_iamge_website_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='website_user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='website_user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='website_user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='pics'),
        ),
        migrations.AlterField(
            model_name='website_user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='website_user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='website_user',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
