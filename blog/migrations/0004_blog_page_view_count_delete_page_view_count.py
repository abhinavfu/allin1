# Generated by Django 4.1.7 on 2023-07-13 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_page_view_count_createpost_post_view_count_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog_page_view_count',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_view_count', models.IntegerField(default=0)),
                ('blog_view_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='Page_view_count',
        ),
    ]
