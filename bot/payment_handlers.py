from aiogram import Router, F
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message
from aiogram.types.input_media import InputMedia
from data_manager import data_manager
from bot.keyboards import get_back_keyboard
import random

router = Router()

@router.callback_query(F.data == "about_full_course")
async def about_full_course_handler(callback: CallbackQuery):
    """Show information about full course"""
    course_info = """
💎 **Полный курс "Путь к внутренней гармонии"**

**📚 Что включено (полная программа):**

**Модуль 1: Основы (уже пройден) ✅**
• Введение в медитацию
• Базовые дыхательные техники
• Первые практики

**Модуль 2: Углубление**
• Медитация любящей доброты
• Сканирование тела
• Работа с эмоциями
• Техники визуализации

**Модуль 3: Продвинутые практики**
• Ходячая медитация
• Медитация в движении
• Трансцендентальные техники
• Работа с чакрами

**Модуль 4: Интеграция**
• Медитация в повседневной жизни
• Построение личной практики
• Работа с сопротивлением
• Поддержание мотивации

**🎁 Бонусы:**
• Библиотека из 500+ аудиозаписей
• Персональный коуч-бот
• Доступ в закрытое сообщество
• Сертификат инструктора медитации

**💫 Результат:**
Через 30 дней у тебя будет устойчивая практика медитации, которая кардинально улучшит качество жизни.

**Стоимость:** 590₽ (скидка 70% только сегодня!)
"""
    
    await callback.message.edit_text(
        text=course_info,
        reply_markup=get_back_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "pay_card")
async def pay_card_handler(callback: CallbackQuery):
    """Handle card payment"""
    prices = [LabeledPrice(label="Полный курс медитации", amount=59000)]  # 590.00 рублей
    
    await callback.message.answer_invoice(
        title="Путь к внутренней гармонии",
        description="Полный курс медитации с 15+ уроками, библиотекой звуков и сертификатом",
        payload="meditation_course_full",
        provider_token="1744374395:TEST:c2588a53275e15616b46",
        currency="RUB",
        prices=prices,
        start_parameter="meditation_course",
        photo_url="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
        photo_width=400,
        photo_height=300
    )

@router.callback_query(F.data == "pay_stars")
async def pay_stars_handler(callback: CallbackQuery):
    """Handle Telegram Stars payment"""
    prices = [LabeledPrice(label="Полный курс медитации", amount=150)]  # 150 stars
    
    await callback.message.answer_invoice(
        title="Путь к внутренней гармонии ⭐",
        description="Полный курс медитации оплата Telegram Stars",
        payload="meditation_course_stars",
        provider_token="",  # Empty for stars
        currency="XTR",  # Telegram Stars currency
        prices=prices,
        start_parameter="meditation_course_stars",
        photo_url="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
        photo_width=400,
        photo_height=300
    )

@router.pre_checkout_query()
async def pre_checkout_handler(query: PreCheckoutQuery):
    """Handle pre-checkout query"""
    await query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment_handler(message: Message):
    """Handle successful payment"""
    user_id = str(message.from_user.id)
    payment = message.successful_payment
    
    # Update user payment status
    await data_manager.update_user(user_id, {"payment_status": "paid"})
    await data_manager.add_achievement(user_id, "course_complete")
    await data_manager.add_coins(user_id, 500)  # Bonus coins
    
    success_images = [
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
        "https://images.unsplash.com/photo-1515279035982-b2b9e5ad2e53?w=800"
    ]
    
    success_text = f"""
🎉 **Поздравляю! Оплата прошла успешно!**

**✅ Детали транзакции:**
• Сумма: {payment.total_amount // 100 if payment.currency == 'RUB' else payment.total_amount} {payment.currency}
• ID: {payment.telegram_payment_charge_id}

**🎁 Что ты получил:**
✨ Доступ ко всем 15+ урокам курса
✨ Библиотеку из 500+ звуков для медитации
✨ Персонального коуч-бота
✨ Сертификат инструктора медитации
✨ 500 бонусных медитативных монет
✨ Пожизненный доступ к материалам

**🏆 Новое достижение:** "Владелец полного курса"

**📱 Как начать:**
Все материалы уже доступны в боте! 
Используй команду /menu для навигации по полному курсу.

Добро пожаловать в семью практикующих медитацию! 🧘‍♀️✨

---
*Это демо-версия. В реальном боте здесь будет доступ к полному курсу.*
"""
    
    await message.answer_photo(
        photo=random.choice(success_images),
        caption=success_text,
        parse_mode="Markdown"
    )