import requests
from django.db.models.signals import post_save
from django.dispatch import receiver

from bot.MESSAGES import MESSAGES
from bot.models import Application
from hotline_agmk.settings import TELEGRAM_API_URL


@receiver(post_save, sender=Application)
def application_status_changed(sender, instance, created, **kwargs):
    if instance.status == Application.Status.completed:
        text = 'Ваша заявка была выполнена ✅\n\n'
        text += (MESSAGES[f'application_detail_{instance.creator.language}']
                 .format('', instance.pk,
                         instance.category.get_name_by_lang(instance.creator.language),
                         instance.comment,
                         instance.created_at.strftime("%d-%m-%Y %H:%M"),
                         MESSAGES[f'status_{instance.status}_{instance.creator.language}']))
        payload = {
            'chat_id': instance.creator.tg_id,
            'text': text
        }
        response = requests.post(TELEGRAM_API_URL, json=payload)
        if response.status_code != 200:
            print(f"Failed to send message. Status code: {response.status_code}")
        else:
            print("Message sent successfully!")
