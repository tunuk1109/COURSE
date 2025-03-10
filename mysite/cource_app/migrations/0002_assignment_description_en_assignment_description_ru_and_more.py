# Generated by Django 5.1.5 on 2025-01-26 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cource_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='description_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='description_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='title_en',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='title_ru',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='category_name_en',
            field=models.CharField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='category_name_ru',
            field=models.CharField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='course',
            name='course_name_en',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='course_name_ru',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='description_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='description_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='title_en',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='title_ru',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='title_en',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='title_ru',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='title_en',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='title_ru',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='bio_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='bio_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='subjects_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='subjects_ru',
            field=models.TextField(null=True),
        ),
    ]
