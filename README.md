# AI Sales Bot — Telegram-витрина для AIBuild

Telegram-бот-витрина для студии разработки AI-ботов. Презентация услуг, кейсы, FAQ, сбор заявок.

## Возможности

### Каталог услуг
- Умные боты 2-в-1 (AI-поддержка + онлайн-запись)
- AI-ассистенты (личный/командный помощник на базе GPT)
- Описание, цены, сроки — всё внутри бота

### Продающие блоки
- Когда нужен AI-бот (боли клиентов)
- Результаты внедрения (цифры и метрики)
- Сравнение: AI-бот vs обычный бот
- Как работаем (процесс от заявки до запуска)

### Кейсы
- Карусель с навигацией (влево/вправо)
- Кнопка "Хочу такое же" на каждом кейсе

### FAQ
- Список частых вопросов с раскрытием по клику

### Сбор заявок (FSM)
- Пошаговая форма: имя → контакт → описание задачи
- Валидация на каждом шаге
- Уведомление админу о новой заявке
- Возможность отмены на любом шаге

### Контакты
- Telegram, WhatsApp, кнопка заявки

## Стек

- Python 3.10+
- aiogram 3.x
- python-dotenv

## Установка

```bash
git clone https://github.com/Shikaro/ai-sales-bot.git
cd ai-sales-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Настройка

Создайте `.env`:

```
BOT_TOKEN=ваш_токен_из_BotFather
ADMIN_ID=ваш_chat_id
ADMIN_USERNAME=ваш_username
WHATSAPP=+7XXXXXXXXXX
EMAIL=your@email.com
```

## Запуск

```bash
python bot.py
```

## Структура

```
ai-sales-bot/
├── .env            — токены и настройки (не в git)
├── bot.py          — точка входа, диспетчер
├── config.py       — загрузка конфигурации из .env
├── handlers.py     — обработчики команд и callback'ов, FSM заявки
├── keyboards.py    — inline-клавиатуры
├── texts.py        — все тексты бота (услуги, кейсы, FAQ)
└── requirements.txt
```

## Автор

Сергей Саплинов — [AIBuild](https://t.me/AI_Build_TOP_BOT)
