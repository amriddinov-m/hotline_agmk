from django.db import models


class EEUser(models.Model):
    class Language(models.TextChoices):
        UZ = 'uz', 'Узбекский язык'
        RU = 'ru', 'Русский язык'
        US = 'us', 'Английский язык'
        IN = 'in', 'Хинди'
        VN = 'vn', 'Вьетнамский'
        TR = 'tr', 'Турецкий язык'

    fullname = models.CharField(max_length=255, verbose_name='ФИО')
    phone = models.CharField(verbose_name='Телефон', max_length=20)
    position = models.CharField(max_length=255, verbose_name='Должность', null=True)
    language = models.CharField(max_length=255, verbose_name='Язык', choices=Language.choices, default=Language.RU)
    tg_id = models.BigIntegerField(verbose_name='Телеграм айди', default=0)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    name_uz = models.CharField(max_length=255, verbose_name='Название UZ', null=True)
    name_ru = models.CharField(max_length=255, verbose_name='Название RU')
    name_us = models.CharField(max_length=255, verbose_name='Название US', null=True)
    name_in = models.CharField(max_length=255, verbose_name='Название IN', null=True)
    name_vn = models.CharField(max_length=255, verbose_name='Название VN', null=True)
    name_tr = models.CharField(max_length=255, verbose_name='Название TR', null=True)

    def __str__(self):
        return self.name_ru

    def get_name_by_lang(self, lang):
        language_mapping = {
            "uz": self.name_uz,
            "ru": self.name_ru,
            "us": self.name_us,
            "in": self.name_in,
            "vn": self.name_vn,
            "tr": self.name_tr,
        }
        return language_mapping[lang]

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Application(models.Model):
    class Status(models.TextChoices):
        created = 'created', 'Направлено на исполнение'
        progress = 'progress', 'В процессе'
        completed = 'completed', 'Выполнено'
    creator = models.ForeignKey('EEUser', on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    comment = models.TextField(verbose_name='Комментарий')
    status = models.CharField(max_length=255, verbose_name='Статус', choices=Status.choices, default=Status.created)
    document = models.FileField(upload_to='file/', verbose_name='Документ', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
