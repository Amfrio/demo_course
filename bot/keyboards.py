from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config import config

def get_start_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for start message"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧘 Узнать о курсе", callback_data="about_course")],
        [InlineKeyboardButton(text="🎯 Мои достижения", callback_data="achievements")],
        [InlineKeyboardButton(text="📊 Моя статистика", callback_data="stats")]
    ])

def get_course_intro_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for course introduction"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌟 Да, хочу научиться!", callback_data="want_to_learn")],
        [InlineKeyboardButton(text="🤔 Расскажи подробнее", callback_data="tell_more")],
        [InlineKeyboardButton(text="📈 Какие будут результаты?", callback_data="results")]
    ])

def get_motivation_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for motivation selection"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="😌 Снизить стресс", callback_data="stress_relief")],
        [InlineKeyboardButton(text="🧠 Улучшить концентрацию", callback_data="focus")],
        [InlineKeyboardButton(text="😴 Лучше спать", callback_data="sleep")]
    ])

def get_experience_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for experience level"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🆕 Новичок", callback_data="beginner")],
        [InlineKeyboardButton(text="🌱 Есть опыт", callback_data="intermediate")],
        [InlineKeyboardButton(text="🧘‍♂️ Опытный", callback_data="advanced")]
    ])

def get_ready_to_start_keyboard() -> InlineKeyboardMarkup:
    """Keyboard to start first lesson"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Начать первый урок!",
                            web_app=WebAppInfo(url=f"{config.webapp_url}/lesson/1"))],
        [InlineKeyboardButton(text="🎁 Получить награду за урок", callback_data="check_lesson_completion")]
    ])

def get_gift_selection_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for gift selection after lesson"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎁", callback_data="gift_1"),
            InlineKeyboardButton(text="🎁", callback_data="gift_2"),
            InlineKeyboardButton(text="🎁", callback_data="gift_3")
        ]
    ])

def get_continue_keyboard() -> InlineKeyboardMarkup:
    """Keyboard to continue or schedule next lesson"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Продолжить сейчас", callback_data="continue_now")],
        [InlineKeyboardButton(text="⏰ Напомнить завтра", callback_data="remind_tomorrow")]
    ])

def get_lesson2_keyboard() -> InlineKeyboardMarkup:
    """Keyboard to start second lesson"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎥 Урок 2: Практика", 
                            web_app=WebAppInfo(url=f"{config.webapp_url}/lesson/2"))],
        [InlineKeyboardButton(text="Что дальше?", callback_data="lesson2_complete")]
    ])

def get_payment_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for payment options"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить тестовой картой", callback_data="pay_card")],
        [InlineKeyboardButton(text="⭐ Оплатить звездами", callback_data="pay_stars")],
        [InlineKeyboardButton(text="ℹ️ О полном курсе", callback_data="about_full_course")]
    ])

def get_back_keyboard() -> InlineKeyboardMarkup:
    """Simple back button"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]
    ])