# Generated by Django 4.2.1 on 2023-10-19 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customregistration',
            name='name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='customregistration',
            name='usertype',
            field=models.CharField(choices=[('hospital', 'Hospital'), ('donor', 'Donor'), ('patient', 'Patient')], default='patient', max_length=10),
        ),
    ]
