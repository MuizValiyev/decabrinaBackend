import asyncio
from aiogram import Bot
from asgiref.sync import sync_to_async
from django.utils.timezone import localtime


async def send_order_notification(order):
    from .config import BOT_TOKEN, CHAT_ID  # внутрь функции, чтобы не вызывался заранее

    bot = Bot(token=BOT_TOKEN)  # ✅ создаём каждый раз

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
        f"📅 Дата: {localtime(order.created_at).strftime('%Y-%m-%d %H:%M')}"
    )

    await bot.send_message(chat_id=CHAT_ID, text=text)
    await bot.session.close()  # ✅ обязательно закрываем сессию


async def send_custom_order_notification(custom_order):
    from .config import BOT_TOKEN, CHAT_ID  # внутрь функции, чтобы не вызывался заранее
    bot = Bot(token=BOT_TOKEN)  # ✅ создаём каждый раз
    parts = []
    if custom_order.model:
        parts.append(f"Модель: {custom_order.model.name}")
    if custom_order.textile:
        parts.append(f"Ткань: {custom_order.textile.name}")
    if custom_order.color:
        parts.append(f"Цвет: {custom_order.color.name}")
    if custom_order.size:
        parts.append(f"Размер: {custom_order.size.label}")

    if custom_order.bust:
        parts.append(f"Обхват груди: {custom_order.bust} см")
    if custom_order.waist:
        parts.append(f"Обхват талии: {custom_order.waist} см")
    if custom_order.hips:
        parts.append(f"Обхват бедер: {custom_order.hips} см")
    if custom_order.height:
        parts.append(f"Рост: {custom_order.height} см")

    address_parts = []
    if custom_order.phone:
        address_parts.append(f"📱 Телефон: {custom_order.phone}")
    if custom_order.city:
        address_parts.append(f"📍 Город: {custom_order.city}")
    if custom_order.address:
        address_parts.append(f"🏠 Адрес: {custom_order.address}")

    comment = f"💬 Комментарий: {custom_order.comment}" if custom_order.comment else ""

    text = (
        f"🧵 Новый кастомный заказ #{custom_order.id}\n"
        f"👤 Пользователь: {custom_order.user.email}\n\n"
        + "\n".join(parts) + "\n\n"
        + "\n".join(address_parts) + "\n\n"
        + (comment + "\n\n" if comment else "")
        + f"📅 Дата: {localtime(custom_order.created_at).strftime('%Y-%m-%d %H:%M')}"
    )

    await bot.send_message(chat_id=CHAT_ID, text=text)
    await bot.session.close()  # ✅ обязательно закрываем сессию
