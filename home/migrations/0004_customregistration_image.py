# Generated by Django 4.2.1 on 2023-10-27 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_customregistration_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customregistration',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]
