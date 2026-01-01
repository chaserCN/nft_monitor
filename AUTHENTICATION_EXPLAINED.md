# Почему нет встроенной аутентификации в portalsmp?

## Как работает аутентификация Portals

Portals использует систему **Telegram Mini Apps** для аутентификации. Это значит:

1. Portals - это бот внутри Telegram (@portals_market_bot)
2. Когда вы открываете Mini App, Telegram создаёт специальный токен
3. Этот токен подтверждает, что вы - реальный пользователь Telegram
4. Токен формата: `tma <длинная_строка_с_данными>`

## Почему библиотека требует authData отдельно?

### Техническая причина:
Чтобы получить токен программно, нужно:
1. **Запустить Telegram клиент** (используя Pyrogram/Telethon)
2. **Эмулировать открытие Mini App** бота @portals_market_bot
3. **Извлечь токен** из ответа Telegram

Это требует:
- `api_id` и `api_hash` от Telegram (получаются на https://my.telegram.org/auth)
- Библиотеку Pyrogram (для работы с Telegram API)
- Логин в ваш Telegram аккаунт (первый раз - код из SMS)

### Почему это не встроено в библиотеку?

1. **Зависимость**: Нужна тяжёлая библиотека Pyrogram (~50MB)
2. **Безопасность**: api_id/api_hash - это чувствительные данные
3. **Первый запуск**: Требуется интерактивный ввод (телефон, код из SMS)
4. **Гибкость**: Разные пользователи могут выбирать способ получения токена

## Два способа получения токена

### Способ 1: Ручной (простой, но токен expires)
```bash
1. Открыть web.telegram.org
2. Найти @portals_market_bot
3. Открыть Mini App
4. DevTools → Network → найти Authorization header
5. Скопировать токен
```

**Плюсы**: Просто, не нужны api_id/api_hash
**Минусы**: Токен живёт 1-7 дней, потом надо обновлять вручную

### Способ 2: Программный (сложнее, но автоматический)
```python
from portalsmp import update_auth
import asyncio

# Один раз получить на https://my.telegram.org/auth
api_id = 12345678
api_hash = "abcdef1234567890"

# Получить токен
token = asyncio.run(update_auth(api_id, api_hash))
```

**Плюсы**: Токен обновляется автоматически, работает долго
**Минусы**: Нужны Telegram credentials, первый раз нужен SMS код

## Что происходит внутри update_auth()

```python
async def update_auth(api_id, api_hash):
    # 1. Создать Telegram клиент
    async with Client("account", api_id, api_hash) as client:
        # 2. Найти бота @portals
        peer = await client.resolve_peer("portals")

        # 3. Запросить информацию о боте
        bot_info = await client.get_users(peer)

        # 4. Открыть Mini App "market"
        web_view = await client.request_app_web_view(
            peer=peer,
            app_name="market"
        )

        # 5. Извлечь токен из URL
        token = extract_token_from_url(web_view.url)

        return f"tma {token}"
```

## Решение для вашего бота

### Вариант A: Ручное обновление (самый простой)
- Раз в неделю вручную обновлять токен через DevTools
- Подходит для тестирования и личного использования

### Вариант B: Автоматическое обновление (рекомендуется)
- Один раз настроить api_id/api_hash
- Бот сам обновляет токен когда нужно
- Подходит для production

### Вариант C: Комбинированный
- Использовать ручной токен как fallback
- Пробовать автообновление при ошибках 401/403
- Уведомлять пользователя если нужно вручную обновить

## Пошаговая настройка автоматической аутентификации

### Шаг 1: Получить Telegram API credentials

1. Откройте https://my.telegram.org/auth
2. Войдите с вашим номером телефона
3. Перейдите в "API development tools"
4. Создайте приложение (любое название)
5. Скопируйте:
   - `api_id` (число)
   - `api_hash` (строка)

### Шаг 2: Добавить в .env

```env
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
```

### Шаг 3: Первый запуск

При первом запуске Pyrogram попросит:
- Ваш номер телефона
- Код из SMS/Telegram
- (Опционально) 2FA пароль

Эти данные сохранятся в файле `account.session` - больше вводить не нужно.

### Шаг 4: Автообновление в коде

```python
from portalsmp import update_auth
import asyncio
import os
from datetime import datetime, timedelta

class PortalsAuth:
    def __init__(self):
        self.token = os.getenv("PORTALS_AUTH_DATA", "")
        self.token_expires = None

    async def get_token(self):
        # Если токен есть и не истёк - использовать его
        if self.token and self.token_expires and datetime.now() < self.token_expires:
            return self.token

        # Иначе - обновить
        api_id = os.getenv("TELEGRAM_API_ID")
        api_hash = os.getenv("TELEGRAM_API_HASH")

        if api_id and api_hash:
            print("Обновление токена...")
            self.token = await update_auth(api_id, api_hash)
            self.token_expires = datetime.now() + timedelta(days=5)
            print("✓ Токен обновлён")
            return self.token
        else:
            raise ValueError("Нужен PORTALS_AUTH_DATA или TELEGRAM_API_ID/API_HASH")
```

## Безопасность

⚠️ **Важно**:
- `api_id` и `api_hash` - это ключи к вашему Telegram аккаунту
- Не публикуйте их в Git
- Добавьте `.env` в `.gitignore`
- Файл `account.session` тоже в `.gitignore`

## Заключение

**Вывод**: Библиотека portalsmp НЕ имеет встроенной аутентификации, потому что:
1. Это требует зависимости от Pyrogram
2. Нужны персональные Telegram credentials
3. Первый запуск требует интерактивного ввода
4. Даёт пользователю выбор: простой ручной способ или автоматический

**Рекомендация**: Реализовать автообновление токена с использованием `update_auth()` - это решит проблему "постоянно вытягивать токен".
