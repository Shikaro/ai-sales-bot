from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ADMIN_USERNAME, WHATSAPP, EMAIL


def main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🤖 AI-ассистент", callback_data="assistant")
    kb.button(text="📅 Booking Bot", callback_data="booking_info")
    kb.button(text="💬 FAQ Bot", callback_data="faq_bot_info")
    kb.button(text="✨ Smart Bot (2в1)", callback_data="smart_bot_info")
    kb.button(text="📈 Кейсы", callback_data="case:0")
    kb.button(text="🛠 Как работаем", callback_data="process")
    kb.button(text="🎯 Бесплатный аудит", callback_data="order")
    kb.button(text="❓ FAQ", callback_data="faq")
    kb.button(text="📞 Контакты", callback_data="contacts")
    kb.adjust(1, 2, 1, 2, 2, 1)
    return kb.as_markup()


def back_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🎯 Бесплатный аудит", callback_data="order")
    kb.button(text="◀ В меню", callback_data="menu")
    kb.adjust(1, 1)
    return kb.as_markup()


def cases_nav(idx: int, total: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    prev_idx = (idx - 1) % total
    next_idx = (idx + 1) % total
    kb.button(text="◀", callback_data=f"case:{prev_idx}")
    kb.button(text=f"{idx + 1}/{total}", callback_data="noop")
    kb.button(text="▶", callback_data=f"case:{next_idx}")
    kb.button(text="🎯 Хочу такое же", callback_data="order")
    kb.button(text="◀ В меню", callback_data="menu")
    kb.adjust(3, 1, 1)
    return kb.as_markup()


def faq_list(count: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for i in range(count):
        kb.button(text=f"❓ Вопрос {i + 1}", callback_data=f"faq:{i}")
    kb.button(text="🎯 Бесплатный аудит", callback_data="order")
    kb.button(text="◀ В меню", callback_data="menu")
    kb.adjust(*([1] * count + [1, 1]))
    return kb.as_markup()


def faq_item() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="◀ К вопросам", callback_data="faq")
    kb.button(text="◀ В меню", callback_data="menu")
    kb.adjust(2)
    return kb.as_markup()


def contacts_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="💬 Написать в Telegram", url=f"https://t.me/{ADMIN_USERNAME}")
    kb.button(text="📱 WhatsApp", url=f"https://wa.me/{WHATSAPP.lstrip('+')}")
    kb.button(text="🎯 Оставить заявку здесь", callback_data="order")
    kb.button(text="◀ В меню", callback_data="menu")
    kb.adjust(1, 1, 1, 1)
    return kb.as_markup()


def order_cancel() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✖ Отменить", callback_data="order_cancel")
    return kb.as_markup()
