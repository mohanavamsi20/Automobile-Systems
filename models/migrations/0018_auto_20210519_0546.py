# Generated by Django 3.0.5 on 2021-05-19 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0017_custom_dealer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='custom',
            options={'ordering': ('make',)},
        ),
        migrations.RemoveField(
            model_name='color',
            name='make',
        ),
        migrations.RemoveField(
            model_name='color',
            name='model',
        ),
        migrations.RemoveField(
            model_name='color',
            name='variant',
        ),
    ]