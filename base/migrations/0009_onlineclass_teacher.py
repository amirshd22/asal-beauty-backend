# Generated by Django 3.2.5 on 2021-08-06 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_onlineclass_hasoff'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlineclass',
            name='teacher',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]