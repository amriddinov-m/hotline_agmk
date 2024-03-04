# Generated by Django 5.0.2 on 2024-02-28 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_application_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_in',
            field=models.CharField(max_length=255, null=True, verbose_name='Название IN'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_tr',
            field=models.CharField(max_length=255, null=True, verbose_name='Название TR'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_us',
            field=models.CharField(max_length=255, null=True, verbose_name='Название US'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_uz',
            field=models.CharField(max_length=255, null=True, verbose_name='Название UZ'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_vn',
            field=models.CharField(max_length=255, null=True, verbose_name='Название VN'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_ru',
            field=models.CharField(max_length=255, verbose_name='Название RU'),
        ),
        migrations.AlterField(
            model_name='eeuser',
            name='language',
            field=models.CharField(choices=[('uz', 'Узбекский язык'), ('ru', 'Русский язык'), ('us', 'Английский язык'), ('in', 'Хинди'), ('vn', 'Вьетнамский'), ('tr', 'Турецкий язык')], default='ru', max_length=255, verbose_name='Язык'),
        ),
    ]