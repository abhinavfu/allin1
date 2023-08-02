# Generated by Django 4.1.7 on 2023-08-01 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_app_date_alter_userprofile_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='appCat',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='subCat',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='AppCategory',
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]
