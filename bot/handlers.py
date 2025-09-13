import asyncio

import aiohttp
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, WebAppData
from aiogram.types.input_media import InputMedia
from data_manager import data_manager
from bot.keyboards import *
import random

router = Router()

# Media content
MEDITATION_IMAGES = [
    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
    "https://images.unsplash.com/photo-1545389336-cf090694435e?w=800",
    "https://images.unsplash.com/photo-1508672019048-805c876b67e2?w=800"
]

@router.message(CommandStart())
async def start_handler(message: Message):
    """Handle /start command"""
    user_id = str(message.from_user.id)
    await data_manager.update_user(user_id,
                                   {
                                       "user_id": user_id,
                                       "current_lesson": 0,
                                       "completed_lessons": [],
                                       "achievements": [],
                                       "total_time": 0,
                                       "last_activity": None,
                                       "meditation_streak": 0,
                                       "coins": 0,
                                       "gifts_received": [],
                                       "quiz_scores": {},
                                       "payment_status": "free"
                                   }
                                   )
    user_data = await data_manager.get_user(user_id)
    
    welcome_text = f"""
🌸 Добро пожаловать в **"Путь к внутренней гармонии"**! 

Привет, {message.from_user.first_name}! 👋

Этот интерактивный курс медитации поможет тебе:
• Обрести внутренний покой 🕊️
• Снизить уровень стресса 😌
• Улучшить концентрацию 🎯
• Найти баланс в жизни ⚖️

💎 **Пройдено уроков:** {len(user_data.get('completed_lessons', []))}
🏆 **Достижений:** {len(user_data.get('achievements', []))}
🪙 **Медитативных монет:** {user_data.get('coins', 0)}

Что хочешь узнать?
"""
    
    await message.answer_photo(
        photo=random.choice(MEDITATION_IMAGES),
        caption=welcome_text,
        reply_markup=get_start_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "about_course")
async def about_course_handler(callback: CallbackQuery):
    """Tell about the course"""
    text = """
🧘‍♀️ **О курсе "Путь к внутренней гармонии"**

Этот курс создан специально для современных людей, которые хотят:

🌟 **Что вы получите:**
• 3 интерактивных урока с видео
• Практические техники медитации
• Звуки природы для практики
• Система достижений и мотивации
• Персональная статистика прогресса

📚 **Структура курса:**
1. **Основы медитации** - теория и первые шаги
2. **Практика дыхания** - видео-урок с техниками
3. **Глубокая медитация** - продвинутые методы

⏱️ **Время прохождения:** 15-20 минут на урок
🎯 **Уровень:** для всех, включая новичков

Готов начать свой путь к гармонии?
"""
    
    await callback.message.edit_caption(
        caption=text,
        reply_markup=get_course_intro_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "tell_more")
async def tell_more_handler(callback: CallbackQuery):
    """Tell more about benefits"""
    text = """
🌈 **Подробнее о пользе медитации:**

**Научно доказанные эффекты:**
• Снижение кортизола (гормона стресса) на 25% 📉
• Улучшение памяти и внимания на 40% 🧠
• Повышение качества сна на 60% 😴
• Укрепление иммунитета 💪

**Что говорят наши ученики:**
💬 "Уже через неделю стал спать лучше!" - Анна
💬 "Наконец научился справляться со стрессом" - Максим
💬 "Чувствую себя более сбалансированным" - Елена

**Особенности нашего подхода:**
🎵 Звуки природы и расслабляющая музыка
🎮 Игровые элементы и достижения
📱 Удобный формат в Telegram
⏰ Гибкий график обучения

Какая цель у тебя?
"""
    
    await callback.message.edit_caption(
        caption=text,
        reply_markup=get_motivation_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "results")
async def results_handler(callback: CallbackQuery):
    """Show expected results"""
    text = """
📈 **Какие результаты ты получишь:**

**После 1-го урока:**
✨ Освоишь базовую технику дыхания
✨ Почувствуешь первое расслабление
✨ Поймешь принципы медитации

**После 2-го урока:**  
🌊 Научишься глубокому расслаблению
🌊 Освоишь технику "4-7-8"
🌊 Сможешь медитировать 5-10 минут

**После полного курса:**
🏆 Регулярная практика медитации
🏆 Управление стрессом и эмоциями
🏆 Улучшение качества жизни
🏆 Внутренняя гармония и покой

⭐ **Бонусы:**
• Библиотека звуков для медитации
• Трекер прогресса и статистика  
• Сообщество единомышленников
• Сертификат о прохождении курса

Определи свой уровень:
"""
    
    await callback.message.edit_caption(
        caption=text,
        reply_markup=get_experience_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.in_(["stress_relief", "focus", "sleep"]))
async def motivation_selected(callback: CallbackQuery):
    """Handle motivation selection"""
    motivations = {
        "stress_relief": "снизить стресс и обрести покой 😌",
        "focus": "улучшить концентрацию и ясность ума 🧠",
        "sleep": "улучшить качество сна и отдыха 😴"
    }
    
    selected = motivations[callback.data]
    
    await data_manager.update_user(
        str(callback.from_user.id), 
        {"motivation": callback.data}
    )
    
    text = f"""
Отлично! Твоя цель - {selected}

Наш курс идеально подходит для достижения этой цели! 
Медитация особенно эффективна именно в этом направлении.

Давай определим твой уровень опыта:
"""
    
    await callback.message.edit_caption(
        caption=text,
        reply_markup=get_experience_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.in_(["beginner", "intermediate", "advanced"]))
async def experience_selected(callback: CallbackQuery):
    """Handle experience level selection"""
    levels = {
        "beginner": "новичок 🆕 - начнем с самых основ!",
        "intermediate": "уже есть опыт 🌱 - углубим знания!",
        "advanced": "опытный практик 🧘‍♂️ - найдем новые грани!"
    }
    
    selected = levels[callback.data]
    
    await data_manager.update_user(
        str(callback.from_user.id), 
        {"experience": callback.data}
    )
    
    text = f"""
Понятно, ты {selected}

🎉 **Персонализация завершена!**

Курс адаптирован под твои потребности. 
Мы подобрали упражнения и темп именно для тебя.

**Что дальше:**
1. Изучишь основы медитации
2. Выполнишь первые упражнения  
3. Получишь подарок за успехи
4. Продолжишь с практическими техниками

🚀 **Готов начать трансформацию?**
Первый урок займет всего 7-10 минут!
"""
    
    await callback.message.edit_caption(
        caption=text,
        reply_markup=get_ready_to_start_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "want_to_learn")
async def want_to_learn_handler(callback: CallbackQuery):
    """Handle direct start"""
    text = """
🔥 **Отлично! Мотивация - это первый шаг к успеху!**

Медитация изменит твою жизнь к лучшему. 
Ты получишь практические инструменты для:

💫 Управления стрессом и эмоциями
💫 Повышения осознанности
💫 Улучшения отношений с собой и другими
💫 Обретения внутренней силы

Давай узнаем, какая цель у тебя главная:
"""
    
    await callback.message.edit_caption(
        caption=text,
        reply_markup=get_motivation_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "achievements")
async def achievements_handler(callback: CallbackQuery):
    """Show user achievements"""
    user_id = str(callback.from_user.id)
    user_data = await data_manager.get_user(user_id)
    
    achievements = user_data.get('achievements', [])
    completed_lessons = user_data.get('completed_lessons', [])
    
    achievement_list = {
        "first_lesson": "🎓 Первый урок",
        "quiz_master": "🧠 Мастер викторин", 
        "daily_practice": "📅 Ежедневная практика",
        "meditation_streak": "🔥 Серия медитаций",
        "course_complete": "🏆 Завершение курса"
    }
    
    text = f"""
🏆 **Твои достижения:**

"""
    
    if achievements:
        for ach in achievements:
            if ach in achievement_list:
                text += f"✅ {achievement_list[ach]}\n"
    else:
        text += "Пока нет достижений, но это только начало! 🌱\n"
    
    text += f"""

📊 **Прогресс:**
• Уроков пройдено: {len(completed_lessons)}/3
• Медитативных монет: {user_data.get('coins', 0)} 🪙
• Общее время практики: {user_data.get('total_time', 0)} мин

{'' if completed_lessons else 'Начни первый урок, чтобы получить первые достижения! 🚀'}
"""
    
    await callback.message.edit_caption(
        caption=text,
        reply_markup=get_back_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "stats")
async def stats_handler(callback: CallbackQuery):
    """Show user statistics"""
    user_id = str(callback.from_user.id)
    user_data = await data_manager.get_user(user_id)
    
    completed_lessons = user_data.get('completed_lessons', [])
    quiz_scores = user_data.get('quiz_scores', {})
    
    text = f"""
📊 **Твоя статистика:**

**Общий прогресс:**
• Завершено уроков: {len(completed_lessons)}/3 ({len(completed_lessons)/3*100:.0f}%)
• Серия медитаций: {user_data.get('meditation_streak', 0)} дней 🔥
• Накоплено монет: {user_data.get('coins', 0)} 🪙

**Результаты викторин:**
"""
    
    if quiz_scores:
        total_score = 0
        for lesson_id, score in quiz_scores.items():
            text += f"• Урок {lesson_id}: {score}/3 ⭐\n"
            total_score += score
        avg_score = total_score / len(quiz_scores)
        text += f"• Средний балл: {avg_score:.1f}/3\n"
    else:
        text += "Пока нет результатов викторин\n"
    
    text += f"""

**Активность:**
• Последняя активность: {user_data.get('last_activity', 'Неизвестно')[:10] if user_data.get('last_activity') else 'Неизвестно'}
• Статус: {'💎 Premium' if user_data.get('payment_status') == 'paid' else '🆓 Free'}

{'' if completed_lessons else 'Начни свой путь медитации уже сегодня! 🧘‍♀️'}
"""
    
    await callback.message.edit_caption(
        caption=text,
        reply_markup=get_back_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "back_to_start")
async def back_to_start_handler(callback: CallbackQuery):
    """Go back to start menu"""
    user_id = str(callback.from_user.id)
    user_data = await data_manager.get_user(user_id)
    
    welcome_text = f"""
🌸 **"Путь к внутренней гармонии"**

Привет снова! 👋

💎 **Пройдено уроков:** {len(user_data.get('completed_lessons', []))}
🏆 **Достижений:** {len(user_data.get('achievements', []))}
🪙 **Медитативных монет:** {user_data.get('coins', 0)}

Что хочешь сделать?
"""
    
    await callback.message.edit_caption(
        caption=welcome_text,
        reply_markup=get_start_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "check_lesson_completion")
async def check_lesson_completion_handler(callback: CallbackQuery):
    user_id = str(callback.from_user.id)

    try:
        from config import config

        async with aiohttp.ClientSession() as session:
            for lesson_id in [1, 2]:
                async with session.get(
                    f"{config.webapp_url}/api/lesson/{lesson_id}/check_completion",
                    params={"user_id": user_id}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("completed"):
                            score = data.get("score", 0)
                            await data_manager.complete_lesson(user_id, lesson_id, score)

                        # Add achievement
                        if lesson_id == 1:
                            await data_manager.add_achievement(user_id, "first_lesson")
                        elif lesson_id == 2:
                            await data_manager.add_achievement(user_id, "quiz_master")

                        # Send congratulations
                        percentage = data.get("percentage", 0)
                        congratulations = f"""
🎉 **Поздравляю с завершением урока {lesson_id}!**

Отличный результат: {score} правильных ответов ({percentage:.0f}%)!

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
                        return

        await callback.answer("Пока нет завершенных уроков. Пройдите урок в WebApp сначала!", show_alert=True)

    except SystemError as e:
        print(f"Error checking lesson completion: {e}")
        await callback.answer("Ошибка проверки завершения урока", show_alert=True)