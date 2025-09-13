import json
import aiofiles
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio
import os

class DataManager:
    def __init__(self, file_path: str = "data/users.json"):
        self.file_path = file_path
        self._lock = asyncio.Lock()
        
    async def load_data(self) -> Dict[str, Any]:
        """Load user data from JSON file"""
        try:
            async with aiofiles.open(self.file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content) if content.strip() else {}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    async def save_data(self, data: Dict[str, Any]) -> None:
        """Save user data to JSON file"""
        async with self._lock:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            async with aiofiles.open(self.file_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2))
    
    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user data"""
        data = await self.load_data()
        return data.get(str(user_id), {
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
        })
    
    async def update_user(self, user_id: str, updates: Dict[str, Any]) -> None:
        """Update user data"""
        data = await self.load_data()
        user_data = data.get(str(user_id), {})
        user_data.update(updates)
        user_data["last_activity"] = datetime.now().isoformat()
        data[str(user_id)] = user_data
        await self.save_data(data)
    
    async def complete_lesson(self, user_id: str, lesson_id: int, quiz_score: int) -> None:
        """Mark lesson as completed"""
        user_data = await self.get_user(user_id)
        if lesson_id not in user_data["completed_lessons"]:
            user_data["completed_lessons"].append(lesson_id)
        user_data["quiz_scores"][str(lesson_id)] = quiz_score
        user_data["current_lesson"] = max(user_data["current_lesson"], lesson_id + 1)
        await self.update_user(user_id, user_data)
    
    async def add_achievement(self, user_id: str, achievement: str) -> bool:
        """Add achievement to user"""
        user_data = await self.get_user(user_id)
        if achievement not in user_data["achievements"]:
            user_data["achievements"].append(achievement)
            await self.update_user(user_id, user_data)
            return True
        return False
    
    async def add_coins(self, user_id: str, amount: int) -> None:
        """Add coins to user balance"""
        user_data = await self.get_user(user_id)
        user_data["coins"] += amount
        await self.update_user(user_id, user_data)

data_manager = DataManager()