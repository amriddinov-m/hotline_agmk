# Generated by Django 5.0.2 on 2024-02-28 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eeuser',
            name='language',
            field=models.CharField(choices=[('kr', 'Узбекский язык'), ('ru', 'Русский язык'), ('en', 'Английский язык'), ('in', 'Хинди'), ('vn', 'Вьетнамский'), ('tr', 'Турецкий язык')], default='ru', max_length=255, verbose_name='Язык'),
        ),
    ]