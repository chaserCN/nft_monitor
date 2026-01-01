"""Telegram bot for NFT gift monitoring."""
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from bot_config import BotConfig
from gift_searcher import GiftSearcher

load_dotenv()


class NFTMonitorBot:
    """NFT Gift Monitor Bot."""

    def __init__(self):
        self.config = BotConfig()
        self.searcher = GiftSearcher()
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.channel_id = os.getenv('TELEGRAM_CHANNEL_ID')

        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN не знайдено в .env")
        if not self.channel_id:
            raise ValueError("TELEGRAM_CHANNEL_ID не знайдено в .env")

        self.app = Application.builder().token(self.bot_token).build()
        self._register_handlers()

    def _register_handlers(self):
        """Register command handlers."""
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("showall", self.cmd_showall))
        self.app.add_handler(CommandHandler("list", self.cmd_list))
        self.app.add_handler(CommandHandler("add", self.cmd_add))
        self.app.add_handler(CommandHandler("delete", self.cmd_delete))
        self.app.add_handler(CommandHandler("setprice", self.cmd_setprice))
        self.app.add_handler(CommandHandler("setinterval", self.cmd_setinterval))
        self.app.add_handler(CommandHandler("pause", self.cmd_pause))
        self.app.add_handler(CommandHandler("resume", self.cmd_resume))
        self.app.add_handler(CommandHandler("stats", self.cmd_stats))
        self.app.add_handler(CommandHandler("image", self.cmd_image))

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_text = """🤖 Бот моніторингу NFT подарунків

Я стежу за маркетплейсом Portals за конкретними NFT подарунками та повідомляю, коли з'являються нові!

📋 Основні команди:
/showall - Показати всі доступні подарунки
/list - Показати відстежувані пари
/add <подарунок>,<модель> - Додати пару до моніторингу
/delete <подарунок>,<модель> - Видалити пару
/image <назва> #<номер> - Показати зображення подарунка

⚙️ Налаштування:
/setprice <сума> - Встановити максимальну ціну
/setinterval <хвилини> - Встановити інтервал перевірки
/pause - Призупинити моніторинг
/resume - Відновити моніторинг

📊 Інформація:
/stats - Переглянути статистику
/help - Детальна довідка

Давайте знайдемо вигідні пропозиції! 🎁"""
        await update.message.reply_text(welcome_text)

    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = """📖 Детальна допомога

🔍 МОНІТОРИНГ:
Бот перевіряє маркетплейс кожні N хвилин на наявність нових подарунків за вашими критеріями.
Коли знайдено, надсилає фото з деталями в канал.

📋 ОСНОВНІ КОМАНДИ:
/start - Привітання та список команд
/help - Детальна допомога
/list - Показати список відстежуваних пар
/showall - Показати ВСІ доступні подарунки (без ліміту ціни)

📝 КЕРУВАННЯ ПАРАМИ:
/add Ionic Dryer,Love Burst
  Додає пару "Ionic Dryer + Love Burst" до моніторингу

/delete Ionic Dryer,Love Burst
  Видаляє цю пару з моніторингу

💰 ФІЛЬТР ЦІНИ:
/setprice 35
  Показувати лише подарунки дешевше 35 TON
  (застосовується до моніторингу, але не до /showall)

⏱ ІНТЕРВАЛ ПЕРЕВІРКИ:
/setinterval 15
  Перевіряти кожні 15 хвилин (за замовчуванням: 10)

🖼️ ПЕРЕГЛЯД ЗОБРАЖЕНЬ:
/image Ionic Dryer #836
  Показує фото конкретного подарунка

📊 СТАТИСТИКА:
/stats
  Показує загальну кількість перевірок, знайдених подарунків, час останньої перевірки

⏸️ ПАУЗА/ВІДНОВЛЕННЯ:
/pause - Зупинити моніторинг тимчасово
/resume - Продовжити моніторинг

Поточний статус: """ + ("✅ Активний" if self.config.is_monitoring_enabled() else "⏸️ На паузі")

        await update.message.reply_text(help_text)

    async def cmd_showall(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /showall command - show all available gifts WITHOUT price filter."""
        await update.message.reply_text("🔍 Шукаю на маркетплейсі (без ліміту ціни)...")

        try:
            combinations = self.config.get_wanted_combinations()
            # NO price filter for showall - use very high limit
            max_price = 999999

            gifts = await self.searcher.search_gifts(combinations, max_price)

            if not gifts:
                await update.message.reply_text("❌ Подарунків не знайдено")
                return

            # Sort by price
            gifts.sort(key=lambda x: float(x.get('price', 999999)))

            # Group by gift+model combination
            by_combo = {}
            for gift in gifts:
                info = self.searcher.format_gift_info(gift)
                key = f"{info['name']} - {info['model']}"
                if key not in by_combo:
                    by_combo[key] = []
                by_combo[key].append(info)

            # Build summary
            summary = f"✅ Знайдено {len(gifts)} подарунків!\n\n"

            for combo, combo_gifts in sorted(by_combo.items()):
                combo_gifts.sort(key=lambda x: float(x['price']))
                cheapest = combo_gifts[0]
                most_expensive = combo_gifts[-1]

                summary += f"📦 {combo} ({len(combo_gifts)} шт.)\n"
                summary += f"   💰 {cheapest['price']} - {most_expensive['price']} TON\n"
                summary += f"   🔗 {cheapest['url']}\n\n"

            # Add top 20 cheapest
            summary += "\n━━━━━━━━━━━━━━━━━━━━\n"
            summary += "💎 ТОП-20 НАЙДЕШЕВШИХ:\n\n"

            for i, gift in enumerate(gifts[:20], 1):
                info = self.searcher.format_gift_info(gift)
                summary += f"{i}. {info['name']} #{info['number']}\n"
                summary += f"   {info['price']} TON | {info['model']} | {info['symbol']} | {info['backdrop']}\n\n"

            if len(gifts) > 20:
                summary += f"... та ще {len(gifts) - 20}"

            await update.message.reply_text(summary)

        except Exception as e:
            await update.message.reply_text(f"❌ Помилка: {str(e)}")

    async def cmd_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /list command - show monitored pairs."""
        combinations = self.config.get_wanted_combinations()
        max_price = self.config.get_max_price()
        interval = self.config.get_check_interval()

        text = f"""📋 Поточна конфігурація моніторингу

🎁 Відстежувані пари ({len(combinations)}):
"""
        for i, (gift, model) in enumerate(combinations, 1):
            text += f"{i}. {gift} + {model}\n"

        text += f"\n💰 Макс. ціна: {max_price} TON"
        text += f"\n⏱ Інтервал перевірки: {interval} хв"
        text += f"\n📊 Статус: {'✅ Активний' if self.config.is_monitoring_enabled() else '⏸️ На паузі'}"

        await update.message.reply_text(text)

    async def cmd_add(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /add command - add gift+model pair."""
        if not context.args:
            await update.message.reply_text(
                "Використання: /add <назва_подарунка>,<модель>\n"
                "Приклад: /add Ionic Dryer,Love Burst"
            )
            return

        # Join all args and split by comma
        pair_str = ' '.join(context.args)
        parts = [p.strip() for p in pair_str.split(',')]

        if len(parts) != 2:
            await update.message.reply_text("❌ Формат: /add <назва_подарунка>,<модель>")
            return

        gift_name, model = parts

        if self.config.add_combination(gift_name, model):
            await update.message.reply_text(
                f"✅ Додано: {gift_name} + {model}\n\n"
                f"Всього пар: {len(self.config.get_wanted_combinations())}"
            )
        else:
            await update.message.reply_text("⚠️ Ця пара вже існує")

    async def cmd_delete(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /delete command - remove gift+model pair."""
        if not context.args:
            await update.message.reply_text(
                "Використання: /delete <назва_подарунка>,<модель>\n"
                "Приклад: /delete Ionic Dryer,Love Burst"
            )
            return

        pair_str = ' '.join(context.args)
        parts = [p.strip() for p in pair_str.split(',')]

        if len(parts) != 2:
            await update.message.reply_text("❌ Формат: /delete <назва_подарунка>,<модель>")
            return

        gift_name, model = parts

        if self.config.remove_combination(gift_name, model):
            await update.message.reply_text(
                f"✅ Видалено: {gift_name} + {model}\n\n"
                f"Всього пар: {len(self.config.get_wanted_combinations())}"
            )
        else:
            await update.message.reply_text("⚠️ Пару не знайдено")

    async def cmd_setprice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /setprice command."""
        if not context.args:
            current = self.config.get_max_price()
            await update.message.reply_text(
                f"Поточна макс. ціна: {current} TON\n\n"
                f"Використання: /setprice <сума>\n"
                f"Приклад: /setprice 35"
            )
            return

        try:
            price = int(context.args[0])
            if price <= 0:
                await update.message.reply_text("❌ Ціна має бути додатною")
                return

            self.config.set_max_price(price)
            await update.message.reply_text(f"✅ Максимальну ціну встановлено: {price} TON")
        except ValueError:
            await update.message.reply_text("❌ Невірна ціна. Використовуйте число.")

    async def cmd_setinterval(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /setinterval command."""
        if not context.args:
            current = self.config.get_check_interval()
            await update.message.reply_text(
                f"Поточний інтервал: {current} хв\n\n"
                f"Використання: /setinterval <хвилини>\n"
                f"Приклад: /setinterval 15"
            )
            return

        try:
            minutes = int(context.args[0])
            if minutes < 1:
                await update.message.reply_text("❌ Інтервал має бути не менше 1 хвилини")
                return

            self.config.set_check_interval(minutes)
            await update.message.reply_text(f"✅ Інтервал перевірки встановлено: {minutes} хв")
        except ValueError:
            await update.message.reply_text("❌ Невірне число")

    async def cmd_pause(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /pause command."""
        if not self.config.is_monitoring_enabled():
            await update.message.reply_text("⚠️ Моніторинг вже призупинено")
            return

        self.config.set_monitoring_enabled(False)
        await update.message.reply_text("⏸️ Моніторинг призупинено")

    async def cmd_resume(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /resume command."""
        if self.config.is_monitoring_enabled():
            await update.message.reply_text("⚠️ Моніторинг вже активний")
            return

        self.config.set_monitoring_enabled(True)
        await update.message.reply_text("▶️ Моніторинг відновлено")

    async def cmd_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command."""
        stats = self.config.get_statistics()

        text = f"""📊 Статистика бота

🔍 Всього перевірок: {stats['total_checks']}
🆕 Знайдено нових подарунків: {stats['total_new_gifts_found']}
🕐 Остання перевірка: {stats['last_check_time'] or 'Ніколи'}

⚙️ Поточні налаштування:
💰 Макс. ціна: {self.config.get_max_price()} TON
⏱ Інтервал: {self.config.get_check_interval()} хв
📋 Відстежуваних пар: {len(self.config.get_wanted_combinations())}
📊 Статус: {'✅ Активний' if self.config.is_monitoring_enabled() else '⏸️ На паузі'}"""

        await update.message.reply_text(text)

    async def cmd_image(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /image command - show gift image."""
        if not context.args or len(context.args) < 2:
            await update.message.reply_text(
                "Використання: /image <назва_подарунка> #<номер>\n"
                "Приклад: /image Ionic Dryer #836"
            )
            return

        # Parse gift name and number
        text = ' '.join(context.args)
        if '#' not in text:
            await update.message.reply_text("❌ Формат: /image <назва_подарунка> #<номер>")
            return

        gift_name, number_part = text.rsplit('#', 1)
        gift_name = gift_name.strip()

        try:
            number = int(number_part.strip())
        except ValueError:
            await update.message.reply_text("❌ Невірний номер подарунка")
            return

        # Search for the gift
        await update.message.reply_text("🔍 Шукаю...")

        try:
            combinations = self.config.get_wanted_combinations()
            # Search without price limit for /image command
            max_price = 999999
            gifts = await self.searcher.search_gifts(combinations, max_price)

            # Find matching gift
            for gift in gifts:
                if (gift.get('name', '').lower() == gift_name.lower() and
                    gift.get('external_collection_number') == number):

                    info = self.searcher.format_gift_info(gift)
                    caption = await self.searcher.format_gift_caption(info)

                    if info['photo_url']:
                        await update.message.reply_photo(
                            photo=info['photo_url'],
                            caption=caption
                        )
                    else:
                        await update.message.reply_text(
                            f"📋 {caption}\n\n❌ Зображення недоступне"
                        )
                    return

            await update.message.reply_text(
                f"❌ Подарунок не знайдено: {gift_name} #{number}"
            )

        except Exception as e:
            await update.message.reply_text(f"❌ Помилка: {str(e)}")

    async def check_and_notify(self):
        """Check for new gifts and notify channel."""
        if not self.config.is_monitoring_enabled():
            return

        try:
            combinations = self.config.get_wanted_combinations()
            max_price = self.config.get_max_price()

            # Search for gifts
            gifts = await self.searcher.search_gifts(combinations, max_price)

            # Update statistics
            self.config.increment_check_count()
            self.config.update_last_check_time(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            if not gifts:
                return

            # Filter out already seen gifts
            seen_ids = self.config.get_seen_gift_ids()
            new_gifts = [g for g in gifts if g.get('id') not in seen_ids]

            if not new_gifts:
                return

            # Sort by price
            new_gifts.sort(key=lambda x: float(x.get('price', 999999)))

            # Update statistics
            self.config.add_new_gifts_found(len(new_gifts))

            # Send notifications
            await self.app.bot.send_message(
                chat_id=self.channel_id,
                text=f"🆕 Знайдено {len(new_gifts)} нових подарунків!"
            )

            # Send each gift as separate message with photo
            for gift in new_gifts:
                info = self.searcher.format_gift_info(gift)
                caption = await self.searcher.format_gift_caption(info)

                if info['photo_url']:
                    await self.app.bot.send_photo(
                        chat_id=self.channel_id,
                        photo=info['photo_url'],
                        caption=caption
                    )
                else:
                    await self.app.bot.send_message(
                        chat_id=self.channel_id,
                        text=caption
                    )

                await asyncio.sleep(0.5)  # Small delay between messages

            # Mark gifts as seen
            new_gift_ids = [g.get('id') for g in new_gifts]
            self.config.mark_gifts_as_seen(new_gift_ids)

        except Exception as e:
            print(f"Помилка в check_and_notify: {e}")
            await self.app.bot.send_message(
                chat_id=self.channel_id,
                text=f"⚠️ Помилка під час перевірки: {str(e)}"
            )

    async def monitoring_loop(self, context: ContextTypes.DEFAULT_TYPE):
        """Periodic monitoring loop."""
        await self.check_and_notify()

    def run(self):
        """Start the bot."""
        # Schedule periodic checks
        job_queue = self.app.job_queue
        interval = self.config.get_check_interval()

        job_queue.run_repeating(
            self.monitoring_loop,
            interval=interval * 60,  # Convert minutes to seconds
            first=10  # First check after 10 seconds
        )

        print(f"🤖 Бот запущено! Перевірка кожні {interval} хвилин")
        print(f"📢 Повідомлення надсилатимуться в канал: {self.channel_id}")

        # Start bot
        self.app.run_polling()


if __name__ == "__main__":
    bot = NFTMonitorBot()
    bot.run()
