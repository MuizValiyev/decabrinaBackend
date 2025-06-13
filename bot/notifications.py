import asyncio
from aiogram import Bot
from .config import BOT_TOKEN, CHAT_ID
from asgiref.sync import sync_to_async

bot = Bot(token=BOT_TOKEN)

async def send_order_notification(order):
    items = await sync_to_async(order.get_items_summary)()

    text = (
        f"🛒 Новый заказ #{order.id}\n"
        f"👤 Пользователь: {order.user.email}\n"
        f"📱 Телефон: {order.phone}\n"
        f"📍 Город: {order.city}\n"
        f"🏠 Адрес: {order.address}\n\n"
        f"📝 Товары: {items}\n"
        f"📅 Дата: {order.created_at.strftime('%Y-%m-%d %H:%M')}"
    )
    await bot.send_message(chat_id=CHAT_ID, text=text)