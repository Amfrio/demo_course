from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

class QuizAnswer(BaseModel):
    question_id: int
    answer: str

class QuizSubmission(BaseModel):
    user_id: str
    lesson_id: int
    answers: List[QuizAnswer]
    completion_time: int

@app.get("/")
async def home():
    """Home page"""
    return {"message": "Meditation Course WebApp", "status": "ruing"}


# Lesson content
LESSONS = {
    1: {
        "title": "Основы медитации",
        "subtitle": "Первые шаги к внутренней гармонии",
        "content": """
        <h3>Что такое медитация?</h3>
        <p>Медитация — это древняя практика тренировки ума, которая помогает достичь состояния глубокого покоя и осознанности. Это не попытка очистить ум от мыслей, а обучение наблюдению за ними без суждения.</p>
        
        <h3>Основные принципы</h3>
        <ul>
            <li><strong>Осознанность</strong> — полное присутствие в настоящем моменте</li>
            <li><strong>Принятие</strong> — безусловное принятие того, что происходит</li>
            <li><strong>Терпение</strong> — понимание, что результаты приходят постепенно</li>
            <li><strong>Регулярность</strong> — ежедневная практика важнее длительности</li>
        </ul>
        
        <h3>Польза медитации</h3>
        <div class="benefits">
            <div class="benefit-item">
                <strong>Снижение стресса</strong>
                <p>Медитация снижает уровень кортизола — гормона стресса</p>
            </div>
            <div class="benefit-item">
                <strong>Улучшение концентрации</strong>
                <p>Тренирует способность удерживать внимание</p>
            </div>
            <div class="benefit-item">
                <strong>Эмоциональное равновесие</strong>
                <p>Помогает управлять эмоциями и реакциями</p>
            </div>
            <div class="benefit-item">
                <strong>Лучший сон</strong>
                <p>Успокаивает нервную систему перед сном</p>
            </div>
        </div>
        
        <h3>Первая практика: Дыхание</h3>
        <p>Начнем с самого простого упражнения:</p>
        <ol>
            <li>Найди удобное положение сидя</li>
            <li>Закрой глаза или мягко сфокусируй взгляд</li>
            <li>Начни замечать свое дыхание</li>
            <li>Не пытайся его изменить — просто наблюдай</li>
            <li>Когда ум отвлечется, мягко верни внимание к дыханию</li>
        </ol>
        
        <div class="meditation-timer">
            <h4>Попробуй сейчас: 3-минутная медитация</h4>
            <button id="start-meditation" class="meditation-btn">🧘‍♀️ Начать медитацию</button>
            <div id="timer" class="timer hidden">
                <div class="timer-display">3:00</div>
                <div class="timer-instruction">Наблюдай за дыханием...</div>
            </div>
        </div>
        """,
        "quiz": [
            {
                "id": 1,
                "question": "Что является главной целью медитации?",
                "options": [
                    "Очистить ум от всех мыслей",
                    "Научиться наблюдать за умом без суждения",
                    "Достичь экстаза и блаженства"
                ],
                "correct": 1
            },
            {
                "id": 2,
                "question": "Что делать, если во время медитации отвлекся?",
                "options": [
                    "Расстроиться и прекратить практику",
                    "Бороться с отвлекающими мыслями",
                    "Мягко вернуть внимание к дыханию"
                ],
                "correct": 2
            },
            {
                "id": 3,
                "question": "Как часто нужно медитировать для получения результата?",
                "options": [
                    "Раз в неделю по часу",
                    "Каждый день хотя бы несколько минут",
                    "Только когда есть проблемы"
                ],
                "correct": 1
            }
        ]
    },
    2: {
        "title": "Дыхательные техники",
        "subtitle": "Практическое освоение техник дыхания",
        "content": """
        <h3>Дыхание как основа медитации</h3>
        <p>Дыхание — это мост между сознательным и бессознательным, между телом и умом. Изучая различные техники дыхания, мы получаем мощный инструмент для управления своим состоянием.</p>
        
        <div class="video-container">
            <h4>Видео-урок: Основные техники дыхания</h4>
            <div class="video-placeholder">
                <div class="video-play-btn">▶️</div>
                <p>Видео-урок будет здесь</p>
                <small>Длительность: 8 минут</small>
            </div>
        </div>
        
        <h3>Техника "4-7-8"</h3>
        <p>Эта техника особенно эффективна для расслабления и засыпания:</p>
        <ol>
            <li><strong>Вдох на 4 счета</strong> через нос</li>
            <li><strong>Задержка на 7 счетов</strong></li>
            <li><strong>Выдох на 8 счетов</strong> через рот</li>
            <li>Повтори цикл 4-8 раз</li>
        </ol>
        
        <div class="breathing-guide">
            <h4>Практика с аудио-гидом</h4>
            <div class="audio-controls">
                <button id="start-breathing" class="breathing-btn">🌊 Начать дыхательную практику</button>
                <div id="breathing-guide" class="breathing-display hidden">
                    <div class="breathing-circle"></div>
                    <div class="breathing-instruction">Приготовься...</div>
                    <div class="breathing-counter">Цикл 1 из 4</div>
                </div>
            </div>
        </div>
        
        <h3>Звуки природы для медитации</h3>
        <p>Природные звуки помогают глубже погрузиться в медитативное состояние:</p>
        
        <div class="nature-sounds">
            <div class="sound-option" data-sound="rain">
                <div class="sound-icon">🌧️</div>
                <h4>Звук дождя</h4>
                <p>Успокаивающий шум дождя</p>
                <button class="play-sound">Слушать</button>
            </div>
            <div class="sound-option" data-sound="ocean">
                <div class="sound-icon">🌊</div>
                <h4>Океанские волны</h4>
                <p>Ритмичный шум прибоя</p>
                <button class="play-sound">Слушать</button>
            </div>
            <div class="sound-option" data-sound="forest">
                <div class="sound-icon">🌲</div>
                <h4>Звуки леса</h4>
                <p>Пение птиц и шелест листьев</p>
                <button class="play-sound">Слушать</button>
            </div>
        </div>
        
        <h3>Медитация с визуализацией</h3>
        <p>Визуализация усиливает эффект медитации:</p>
        <div class="visualization-guide">
            <p><strong>Упражнение "Золотой свет":</strong></p>
            <ol>
                <li>Закрой глаза и представь теплый золотистый свет</li>
                <li>Этот свет входит в тебя с каждым вдохом</li>
                <li>Свет заполняет все твое тело, принося покой</li>
                <li>С выдохом отпускай напряжение и тревоги</li>
            </ol>
        </div>
        """,
        "quiz": [
            {
                "id": 1,
                "question": "В технике дыхания '4-7-8' на сколько счетов делается вдох?",
                "options": ["4", "7", "8"],
                "correct": 0
            },
            {
                "id": 2,
                "question": "Какие звуки наиболее эффективны для медитации?",
                "options": [
                    "Громкая музыка",
                    "Звуки природы", 
                    "Речь и разговоры"
                ],
                "correct": 1
            },
            {
                "id": 3,
                "question": "Что такое визуализация в медитации?",
                "options": [
                    "Просмотр видео во время практики",
                    "Создание мысленных образов для усиления эффекта",
                    "Рисование после медитации"
                ],
                "correct": 1
            }
        ]
    }
}

@app.get("/lesson/{lesson_id}", response_class=HTMLResponse)
async def get_lesson(request: Request, lesson_id: int):
    """Get lesson page"""
    if lesson_id not in LESSONS:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    lesson = LESSONS[lesson_id]
    return templates.TemplateResponse("lesson.html", {
        "request": request,
        "lesson_id": lesson_id,
        "lesson": lesson
    })

@app.post("/api/submit-quiz")
async def submit_quiz(request: Request):
    """Submit quiz answers"""
    print("=== ПОЛУЧЕН ЗАПРОС НА /api/submit-quiz ===")

    try:
        # Read raw request data
        body = await request.body()
        print(f"RAW BODY: {body}")

        if not body:
            print("ОШИБКА: Тело запроса пустое!")
            raise HTTPException(status_code=400, detail="Empty request body")

        # Parse JSON manually
        import json
        data = json.loads(body.decode('utf-8'))
        print(f"PARSED DATA: {data}")

        # Create QuizSubmission from parsed data
        submission = QuizSubmission(**data)
        print(f"SUBMISSION CREATED: user={submission.user_id}, lesson={submission.lesson_id}")
        print(f"ANSWERS: {submission.answers}")

        lesson = LESSONS.get(submission.lesson_id)
        if not lesson:
            print(f"ОШИБКА: Урок {submission.lesson_id} не найден!")
            raise HTTPException(status_code=404, detail="Lesson not found")

        print(f"УРОК НАЙДЕН: {lesson['title']}")

    except Exception as e:
        print(f"КРИТИЧЕСКАЯ ОШИБКА: {type(e).__name__}: {str(e)}")
        import traceback
        print(f"TRACEBACK: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

    # Calculate score
    correct_answers = 0
    total_questions = len(lesson["quiz"])

    for answer in submission.answers:
        question = next((q for q in lesson["quiz"] if q["id"] == answer.question_id), None)
        if question and question["options"][question["correct"]] == answer.answer:
            correct_answers += 1

    score = correct_answers
    percentage = (correct_answers / total_questions) * 100

    print(f"Результат: {score}/{total_questions} ({percentage}%)")

    # Here you would normally save to database
    # For demo, we'll just return the result

    return JSONResponse({
        "success": True,
        "score": score,
        "total": total_questions,
        "percentage": percentage,
        "message": get_score_message(percentage),
        "lesson_completed": True,
        "lesson_id": submission.lesson_id
    })

def get_score_message(percentage: float) -> str:
    """Get message based on score percentage"""
    if percentage >= 100:
        return "🌟 Превосходно! Ты полностью освоил материал!"
    elif percentage >= 80:
        return "🎉 Отлично! Ты хорошо разобрался в теме!"
    elif percentage >= 60:
        return "👍 Хорошо! Есть над чем поработать, но основы усвоены!"
    else:
        return "📚 Стоит повторить материал урока еще раз!"

@app.get("/api/lesson/{lesson_id}/progress")
async def get_lesson_progress(lesson_id: int, user_id: str):
    """Get user progress for lesson"""
    # In real app, fetch from database
    return JSONResponse({
        "completed": False,
        "score": None,
        "time_spent": 0
    })

# Simple in-memory storage for demo
completed_lessons = {}

class LessonCompletionRequest(BaseModel):
    user_id: str
    score: int
    percentage: float

@app.post("/api/lesson/{lesson_id}/complete")
async def complete_lesson(lesson_id: int, request: LessonCompletionRequest):
    """Mark lesson as completed"""
    print(f"Получен запрос на завершение урока {lesson_id} для пользователя {request.user_id}")

    completed_lessons[f"{request.user_id}_{lesson_id}"] = {
        "lesson_id": lesson_id,
        "score": request.score,
        "percentage": request.percentage,
        "completed_at": "2024-01-01"  # Demo timestamp
    }

    print(f"Урок {lesson_id} отмечен как завершенный для пользователя {request.user_id}")

    print(completed_lessons)
    return JSONResponse({
        "success": True,
        "message": "Lesson marked as completed"
    })

@app.get("/api/lesson/{lesson_id}/check_completion")
async def check_lesson_completion(lesson_id: int, user_id: str = ""):
    """Check if lesson is completed by user"""
    if not user_id:
        return JSONResponse({"completed": False})

    key = f"{user_id}_{lesson_id}"
    completion_data = completed_lessons.get(key)

    if completion_data:
        return JSONResponse({
            "completed": True,
            "score": completion_data["score"],
            "percentage": completion_data["percentage"]
        })
    else:
        return JSONResponse({"completed": False})

# Catch all other routes (put at the end)
@app.get("/{filename}")
async def catch_static_files(filename: str):
    """Catch requests for missing static files"""
    if filename.endswith(('.js', '.css', '.map', '.png', '.jpg', '.ico')):
        raise HTTPException(status_code=404, detail=f"Static file not found: {filename}")
    raise HTTPException(status_code=404, detail="Page not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)