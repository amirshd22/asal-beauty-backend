# Generated by Django 3.2.5 on 2021-08-06 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20210804_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='classUrl',
        ),
        migrations.AddField(
            model_name='onlineclass',
            name='roomId',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='onlineclass',
            name='url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
