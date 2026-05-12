import logging

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest

import texts
import keyboards as kb
from config import ADMIN_ID, ADMIN_USERNAME

router = Router()
log = logging.getLogger("handlers")


class OrderForm(StatesGroup):
    name = State()
    contact = State()
    task = State()


async def _edit_or_send(cb: CallbackQuery, text: str, markup):
    try:
        await cb.message.edit_text(text, reply_markup=markup)
    except TelegramBadRequest as e:
        log.warning("edit_text failed (%s) — fallback to answer", e)
        try:
            await cb.message.answer(text, reply_markup=markup)
        except Exception as e2:
            log.exception("answer also failed: %s", e2)
            await cb.message.answer(text)
    await cb.answer()


@router.message(CommandStart())
async def cmd_start(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(texts.START, reply_markup=kb.main_menu())


@router.message(Command("menu"))
async def cmd_menu(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(texts.START, reply_markup=kb.main_menu())


@router.message(Command("id"))
async def cmd_id(msg: Message) -> None:
    await msg.answer(f"Ваш chat_id: <code>{msg.from_user.id}</code>")


@router.callback_query(F.data == "menu")
async def cb_menu(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await _edit_or_send(cb, texts.START, kb.main_menu())


@router.callback_query(F.data == "noop")
async def cb_noop(cb: CallbackQuery) -> None:
    await cb.answer()


@router.callback_query(F.data == "pain")
async def cb_pain(cb: CallbackQuery) -> None:
    await _edit_or_send(cb, texts.PAIN, kb.back_menu())


@router.callback_query(F.data == "services")
async def cb_services(cb: CallbackQuery) -> None:
    await _edit_or_send(cb, texts.SERVICES, kb.back_menu())


@router.callback_query(F.data == "assistant")
async def cb_assistant(cb: CallbackQuery) -> None:
    await _edit_or_send(cb, texts.ASSISTANT, kb.back_menu())


@router.callback_query(F.data == "results")
async def cb_results(cb: CallbackQuery) -> None:
    await _edit_or_send(cb, texts.RESULTS, kb.back_menu())


@router.callback_query(F.data == "compare")
async def cb_compare(cb: CallbackQuery) -> None:
    await _edit_or_send(cb, texts.COMPARE, kb.back_menu())


@router.callback_query(F.data == "process")
async def cb_process(cb: CallbackQuery) -> None:
    await _edit_or_send(cb, texts.PROCESS, kb.back_menu())


@router.callback_query(F.data == "contacts")
async def cb_contacts(cb: CallbackQuery) -> None:
    await _edit_or_send(cb, texts.CONTACTS, kb.contacts_kb())


@router.callback_query(F.data.startswith("case:"))
async def cb_case(cb: CallbackQuery) -> None:
    idx = int(cb.data.split(":", 1)[1])
    total = len(texts.CASES)
    idx = idx % total
    await _edit_or_send(cb, texts.CASES[idx], kb.cases_nav(idx, total))


@router.callback_query(F.data == "faq")
async def cb_faq_list(cb: CallbackQuery) -> None:
    lines = ["<b>Частые вопросы</b>\n"]
    for i, (q, _) in enumerate(texts.FAQ_ITEMS, 1):
        lines.append(f"{i}. {q}")
    await _edit_or_send(cb, "\n".join(lines), kb.faq_list(len(texts.FAQ_ITEMS)))


@router.callback_query(F.data.startswith("faq:"))
async def cb_faq_item(cb: CallbackQuery) -> None:
    idx = int(cb.data.split(":", 1)[1])
    if not 0 <= idx < len(texts.FAQ_ITEMS):
        await cb.answer()
        return
    q, a = texts.FAQ_ITEMS[idx]
    await _edit_or_send(cb, f"<b>{q}</b>\n\n{a}", kb.faq_item())


@router.callback_query(F.data == "order")
async def cb_order_start(cb: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(OrderForm.name)
    try:
        await cb.message.edit_text(texts.ORDER_INTRO, reply_markup=kb.order_cancel())
    except TelegramBadRequest:
        await cb.message.answer(texts.ORDER_INTRO, reply_markup=kb.order_cancel())
    await cb.answer()


@router.callback_query(F.data == "order_cancel")
async def cb_order_cancel(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await _edit_or_send(cb, texts.ORDER_CANCELLED, kb.main_menu())


@router.message(OrderForm.name, F.text)
async def order_name(msg: Message, state: FSMContext) -> None:
    name = msg.text.strip()
    if len(name) < 2 or len(name) > 80:
        await msg.answer("Имя слишком короткое или длинное. Попробуйте ещё раз.")
        return
    await state.update_data(name=name)
    await state.set_state(OrderForm.contact)
    await msg.answer(texts.ORDER_ASK_CONTACT, reply_markup=kb.order_cancel())


@router.message(OrderForm.contact, F.text)
async def order_contact(msg: Message, state: FSMContext) -> None:
    contact = msg.text.strip()
    if len(contact) < 4 or len(contact) > 120:
        await msg.answer("Контакт похож на ошибочный. Укажите @username или телефон.")
        return
    await state.update_data(contact=contact)
    await state.set_state(OrderForm.task)
    await msg.answer(texts.ORDER_ASK_TASK, reply_markup=kb.order_cancel())


@router.message(OrderForm.task, F.text)
async def order_task(msg: Message, state: FSMContext, bot: Bot) -> None:
    task = msg.text.strip()
    if len(task) < 5:
        await msg.answer("Опишите задачу хотя бы парой предложений.")
        return
    data = await state.get_data()
    name = data.get("name", "—")
    contact = data.get("contact", "—")
    user = msg.from_user
    tg_link = f"@{user.username}" if user.username else f"id{user.id}"

    summary = (
        "🔥 <b>Новая заявка с бота</b>\n\n"
        f"<b>Имя:</b> {name}\n"
        f"<b>Контакт:</b> {contact}\n"
        f"<b>Telegram:</b> {tg_link} (id <code>{user.id}</code>)\n\n"
        f"<b>Задача:</b>\n{task}"
    )

    delivered = False
    if ADMIN_ID:
        try:
            await bot.send_message(ADMIN_ID, summary)
            delivered = True
        except Exception as e:
            log.exception("Не смог отправить заявку админу: %s", e)
    else:
        log.warning("ADMIN_ID не задан — заявка только в логах:\n%s", summary)

    await state.clear()
    await msg.answer(texts.ORDER_DONE, reply_markup=kb.main_menu())

    if not delivered:
        log.info("ЗАЯВКА (не доставлена админу):\n%s", summary)




@router.callback_query(F.data == 'booking_info')
async def cb_booking_info(cb: CallbackQuery) -> None:
    await _edit_or_send(cb, texts.BOOKING_INFO, kb.back_menu())


@router.callback_query(F.data == 'faq_bot_info')
async def cb_faq_bot_info(cb: CallbackQuery) -> None:
    await _edit_or_send(cb, texts.FAQ_BOT_INFO, kb.back_menu())


@router.callback_query(F.data == 'smart_bot_info')
async def cb_smart_bot_info(cb: CallbackQuery) -> None:
    await _edit_or_send(cb, texts.SMART_BOT_INFO, kb.back_menu())

@router.message()
async def fallback(msg: Message) -> None:
    await msg.answer(texts.UNKNOWN, reply_markup=kb.main_menu())
