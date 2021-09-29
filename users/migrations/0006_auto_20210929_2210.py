# Generated by Django 3.2.6 on 2021-09-29 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_userprofile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='domain',
            field=models.CharField(blank=True, max_length=128, verbose_name='страница в вк'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='langs',
            field=models.CharField(blank=True, max_length=256, verbose_name='языки'),
        ),
    ]
