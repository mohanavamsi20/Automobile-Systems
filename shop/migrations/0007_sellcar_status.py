# Generated by Django 3.0.5 on 2021-05-17 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_buycar'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellcar',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
