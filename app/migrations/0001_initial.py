# Generated by Django 4.1.7 on 2023-07-14 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('link', models.URLField(blank=True, default=None, null=True)),
                ('points', models.IntegerField()),
                ('picapp', models.ImageField(blank=True, default=None, null=True, upload_to='app/images/admin/')),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='App_page_view_count',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_home_view_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='AppCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('name', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screenshot', models.ImageField(blank=True, default=None, null=True, upload_to='app/images/user/')),
                ('date', models.DateTimeField(auto_now=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.app')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='app',
            name='appCat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.appcategory'),
        ),
        migrations.AddField(
            model_name='app',
            name='subCat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.subcategory'),
        ),
    ]