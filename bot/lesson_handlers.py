import asyncio
import random
from aiogram import Router, F
from aiogram.types import CallbackQuery
from data_manager import data_manager
from bot.keyboards import *

router = Router()

# Gift content
GIFTS = {
    "gift_1": {
        "name": "🎵 Звуки дождя для медитации",
        "description": "10-минутная аудиозапись звуков дождя для глубокого расслабления",
        "coins": 50
    },
    "gift_2": {
        "name": "📖 Мини-урок о чакрах", 
        "description": "Дополнительный урок о энергетических центрах и их балансировке",
        "coins": 30
    },
    "gift_3": {
        "name": "🪙 Медитативные монеты",
        "description": "100 бонусных монет для разблокировки контента",
        "coins": 100
    }
}

@router.callback_query(F.data.startswith("lesson_complete_"))
async def lesson_complete_handler(callback: CallbackQuery):
    """Handle lesson completion from webapp"""
    lesson_id = int(callback.data.split("_")[-1])
    user_id = str(callback.from_user.id)
    
    # Add achievement for first lesson
    if lesson_id == 1:
        achievement_added = await data_manager.add_achievement(user_id, "first_lesson")
        if achievement_added:
            await callback.answer("🎓 Достижение разблокировано: Первый урок!", show_alert=True)
    
    congratulations = f"""
🎉 **Поздравляю с завершением урока {lesson_id}!**

Ты сделал важный шаг на пути к внутренней гармонии! 
Твоя практика медитации уже начала приносить пользу.

💫 **Что произошло:**
• Нейронные связи в мозге укрепились
• Уровень стресса снизился
• Осознанность повысилась

🎁 **Время для подарка!**
За твои старания ты заслужил награду.
Выбери один из трех подарков:
"""
    
    await callback.message.answer(
        text=congratulations,
        reply_markup=get_gift_selection_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("gift_"))
async def gift_selection_handler(callback: CallbackQuery):
    """Handle gift selection"""
    gift_id = callback.data
    user_id = str(callback.from_user.id)
    
    gift = GIFTS[gift_id]
    
    # Add gift to user data and coins
    await data_manager.add_coins(user_id, gift["coins"])
    user_data = await data_manager.get_user(user_id)
    user_data.setdefault("gifts_received", []).append(gift_id)
    await data_manager.update_user(user_id, user_data)
    
    gift_text = f"""
🎁 **Отличный выбор!**

Ты получил: **{gift["name"]}**

{gift["description"]}

💰 **+{gift["coins"]} медитативных монет**
🪙 **Всего монет:** {user_data.get('coins', 0) + gift["coins"]}

✨ Подарки помогут тебе глубже погрузиться в практику медитации и получить максимум пользы!

**Что дальше?**
Можешь продолжить обучение прямо сейчас или установить напоминание на завтра.
"""
    
    await callback.message.edit_text(
        text=gift_text,
        reply_markup=get_continue_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "continue_now")
async def continue_now_handler(callback: CallbackQuery):
    """Continue with next lesson immediately"""
    user_id = str(callback.from_user.id)
    user_data = await data_manager.get_user(user_id)
    current_lesson = user_data.get('current_lesson', 1)
    
    if current_lesson == 2:
        next_lesson_text = """
🎥 **Урок 2: Практика дыхательных техник**

Отлично! Продолжаем погружение в мир медитации.

Во втором уроке ты:
• Изучишь технику "4-7-8" для быстрого расслабления
• Посмотришь видео с практическими упражнениями  
• Научишься медитировать под звуки природы
• Освоишь визуализацию для глубокого покоя

⏱️ **Длительность:** 10-12 минут
🎯 **Сложность:** Базовая
🎵 **Включает:** Видео + звуки природы

Готов к следующему шагу трансформации?
"""
        
        await callback.message.edit_text(
            text=next_lesson_text,
            reply_markup=get_lesson2_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await show_payment_screen(callback)

@router.callback_query(F.data == "remind_tomorrow")
async def remind_tomorrow_handler(callback: CallbackQuery):
    """Set reminder for tomorrow (demo version)"""
    await callback.message.edit_text(
        text="""
⏰ **Напоминание установлено!**

Завтра в это же время я напомню тебе о продолжении курса.

🧘‍♀️ **Рекомендация:**
До следующего урока попробуй применить изученную технику дыхания:
• Утром после пробуждения (5 минут)
• Вечером перед сном (5 минут)
• В моменты стресса (2-3 минуты)

До встречи завтра! 👋

---
📝 **Демо-режим:** Для демонстрации напоминание придет через минуту, а не завтра.
""",
        parse_mode="Markdown"
    )
    
    # Demo reminder after 1 minute
    await asyncio.sleep(60)
    
    remind_text = """
🔔 **Время для медитации!**

Привет! Как обещал, напоминаю о продолжении курса медитации.

🌅 **Новый день - новые возможности!**
Готов продолжить свой путь к внутренней гармонии?

Во втором уроке тебя ждет:
• Практическое видео с техниками дыхания
• Звуки природы для медитации
• Более глубокие упражнения

Начнем? 🚀
"""
    
    await callback.message.answer(
        text=remind_text,
        reply_markup=get_lesson2_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("lesson2_complete"))
async def lesson2_complete_handler(callback: CallbackQuery):
    """Handle lesson 2 completion"""
    user_id = str(callback.from_user.id)
    
    # Add quiz master achievement
    await data_manager.add_achievement(user_id, "quiz_master")
    
    completion_text = """
🌟 **Превосходно! Урок 2 завершен!**

Ты освоил практические техники дыхания и медитации!

📈 **Твой прогресс:**
✅ Основы медитации изучены
✅ Дыхательные техники освоены  
✅ Практика со звуками природы
✅ 2/3 уроков завершено

🎊 **Вводная часть курса завершена!**

Ты получил крепкую основу для самостоятельной практики медитации. Но это только начало удивительного путешествия к внутренней гармонии!

💎 **Полный курс включает:**
• 15+ дополнительных уроков
• Продвинутые техники медитации
• Персональные планы практики
• Библиотеку звуков (500+ записей)
• Сертификат инструктора

Хочешь продолжить трансформацию?
"""
    
    await callback.message.answer(
        text=completion_text,
        reply_markup=get_payment_keyboard(),
        parse_mode="Markdown"
    )

async def show_payment_screen(callback: CallbackQuery):
    """Show payment options"""
    payment_text = """
💎 **Время перейти на новый уровень!**

Вводная часть курса завершена. Ты уже почувствовал силу медитации!

**Полный курс "Путь к внутренней гармонии" включает:**

🧘‍♀️ **15+ дополнительных уроков:**
• Медитация любящей доброты
• Сканирование тела
• Ходячая медитация
• Медитация в движении
• Трансцендентальные техники

🎵 **Библиотека звуков (500+ записей):**
• Звуки природы в HD качестве
• Бинауральные биты для глубокой медитации
• Мантры и поющие чаши
• Классическая медитативная музыка

📱 **Продвинутые возможности:**
• Персональный трекер прогресса
• Напоминания о практике
• Сообщество практикующих
• Сертификат о прохождении

💰 **Стоимость:** 590₽ (вместо 1990₽)
⭐ **Или:** 150 Telegram Stars

Выбери удобный способ оплаты:
"""
    
    await callback.message.answer(
        text=payment_text,
        reply_markup=get_payment_keyboard(),
        parse_mode="Markdown"
    )