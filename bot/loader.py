from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from django.conf import settings

from bot.middleware import PrintFullNameMiddleware

form_router = Router()

bot = Bot(token=settings.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_router(form_router)

# form_router.message.middleware(PrintFullNameMiddleware())


__all__ = ['bot', 'storage', 'dp']
