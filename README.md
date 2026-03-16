# 🤖 Telegram Bot Constructor

Платформа для создания и запуска Telegram-ботов без кода.

## 🚀 Быстрый старт (Docker)

```bash
# 1. Настроить окружение
cp .env.example .env
# Заполнить BOT_TOKEN, ADMIN_IDS, BOT_USERNAME

# 2. Запустить
docker-compose up -d --build

# 3. Логи
docker-compose logs -f app

# 4. Остановить
docker-compose down
```

## 💻 Локальный запуск (dev / SQLite)

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows

pip install -r requirements.txt

# В .env установить:
# DATABASE_URL=sqlite:///./bot_constructor.db

python main.py
```

## 🗃 Миграции Alembic

```bash
alembic upgrade head                              # применить
alembic revision --autogenerate -m "описание"    # создать новую
alembic downgrade -1                              # откатить
alembic current                                   # статус
```

## 🔑 Настройка Telegram Payments

1. @BotFather → Bot Settings → Payments → выбрать провайдера
2. Получить токен → добавить в `.env`: `PAYMENT_PROVIDER_TOKEN=...`

## 🤖 Шаблоны ботов

| Шаблон | Цена | Описание |
|--------|------|----------|
| 📈 Инвест-бот | 150 ₽ | Депозиты, выводы, рефералы |
| 👥 Реферальный бот | 150 ₽ | Реф. программа с выплатами |
| 🛒 Бот авто-продаж | 150 ₽ | Магазин, каталог, автодоставка |
| ✉️ Бот обратной связи | 100 ₽ | Сбор сообщений + ответы |

## 📋 Переменные окружения

| Переменная | Описание |
|-----------|----------|
| `BOT_TOKEN` | Токен главного бота от @BotFather |
| `BOT_USERNAME` | Username бота без @ |
| `ADMIN_IDS` | ID администраторов через запятую |
| `DATABASE_URL` | URL базы данных |
| `PAYMENT_PROVIDER_TOKEN` | Токен платёжного провайдера |
| `REFERRAL_PERCENT` | % реферальной награды (default: 10) |
| `VIP_PRICE` | Цена VIP тарифа в ₽ (default: 200) |
| `VIP_REFUND` | Возврат при отмене VIP (default: 100) |
| `HOSTING_DAILY_COST` | Стоимость хостинга в день (default: 0.72) |

## 📁 Структура

```
tg_bot_constructor/
├── app/
│   ├── bot/            # Главный бот + хэндлеры + клавиатуры
│   ├── core/           # Config, DB, Logger
│   ├── models/         # SQLAlchemy модели
│   ├── services/       # Бизнес-логика
│   ├── runtime/        # Движок запуска дочерних ботов
│   ├── payments/       # PaymentProvider (Invoice + Manual)
│   ├── templates/      # Шаблоны дочерних ботов
│   └── scheduler/      # APScheduler задачи
├── alembic/            # Миграции БД
├── main.py             # Точка входа
├── docker-compose.yml
└── .env.example
```

## ⚠️ TODO перед продакшном

- [ ] Указать реквизиты для ручного пополнения
- [ ] Настроить `PAYMENT_PROVIDER_TOKEN`
- [ ] Сменить пароль PostgreSQL в `docker-compose.yml`
- [ ] Заполнить ссылки проекта в `.env`
