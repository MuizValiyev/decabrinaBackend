import asyncio
from aiogram import Bot
from .config import BOT_TOKEN, CHAT_ID
from asgiref.sync import sync_to_async

bot = Bot(token=BOT_TOKEN)

async def send_order_notification(order):
    order_items = await sync_to_async(list)(order.items.select_related('product', 'size', 'color', 'textile').all())

    items_text = ""
    for item in order_items:
        parts = [f"{item.product.name} x{item.quantity}"]
        if item.size:
            parts.append(f"Размер: {item.size.size_label}")  
        if item.color:
            parts.append(f"Цвет: {item.color.name}")
        if item.textile:
            parts.append(f"Ткань: {item.textile.name}")
        items_text += "• " + ", ".join(parts) + "\n"

    text = (
        f"🛒 Новый заказ #{order.id}\n"
        f"👤 Пользователь: {order.user.email}\n"
        f"📱 Телефон: {order.phone}\n"
        f"📍 Город: {order.city}\n"
        f"🏠 Адрес: {order.address}\n\n"
        f"📝 Товары:\n{items_text}"
        f"📅 Дата: {order.created_at.strftime('%Y-%m-%d %H:%M')}"
    )

    await bot.send_message(chat_id=CHAT_ID, text=text)
