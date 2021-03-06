# Generated by Django 3.2.5 on 2021-08-04 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_userprofile_onlineclass'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlineclass',
            name='totalPrice',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registerstudentforonlineclass',
            name='totalPrice',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='onlineClass',
            field=models.ManyToManyField(blank=True, related_name='onlineClass', to='base.OnlineClass'),
        ),
    ]
