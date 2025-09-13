// Meditation webapp JavaScript functionality

class MeditationApp {
    constructor() {
        this.tg = window.Telegram?.WebApp;
        this.audioContext = null;
        this.currentAudio = null;
        this.achievements = [];
        this.stats = {
            totalTime: 0,
            sessionsCompleted: 0,
            streak: 0
        };
        
        this.init();
    }
    
    init() {
        if (this.tg) {
            this.tg.expand();
            this.tg.ready();
            this.tg.MainButton.hide();
        }
        
        this.setupAudioContext();
        this.bindEvents();
        this.loadUserData();
    }
    
    setupAudioContext() {
        // Initialize Web Audio API for better audio control
        if (window.AudioContext || window.webkitAudioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    }
    
    bindEvents() {
        // Meditation timer events
        const meditationBtn = document.getElementById('start-meditation');
        if (meditationBtn) {
            meditationBtn.addEventListener('click', () => this.startMeditation());
        }
        
        // Breathing exercise events  
        const breathingBtn = document.getElementById('start-breathing');
        if (breathingBtn) {
            breathingBtn.addEventListener('click', () => this.startBreathing());
        }
        
        // Sound player events
        document.querySelectorAll('.play-sound').forEach(btn => {
            btn.addEventListener('click', (e) => this.playNatureSound(e));
        });
        
        // Progress tracking
        window.addEventListener('scroll', () => this.updateProgress());
        
        // Completion events
        const completeBtn = document.getElementById('complete-lesson');
        if (completeBtn) {
            completeBtn.addEventListener('click', () => this.completeLesson());
        }
    }
    
    async loadUserData() {
        // Load user progress from localStorage or API
        const userData = localStorage.getItem('meditationUserData');
        if (userData) {
            const data = JSON.parse(userData);
            this.stats = { ...this.stats, ...data.stats };
            this.achievements = data.achievements || [];
        }
    }
    
    saveUserData() {
        const userData = {
            stats: this.stats,
            achievements: this.achievements,
            lastActivity: new Date().toISOString()
        };
        localStorage.setItem('meditationUserData', JSON.stringify(userData));
    }
    
    startMeditation() {
        const btn = document.getElementById('start-meditation');
        const timer = document.getElementById('timer');
        
        btn.style.display = 'none';
        timer.classList.remove('hidden');
        
        this.runMeditationTimer(180); // 3 minutes
        this.playAmbientSound('meditation');
    }
    
    runMeditationTimer(duration) {
        const timerDisplay = document.querySelector('.timer-display');
        const instruction = document.querySelector('.timer-instruction');
        
        let timeLeft = duration;
        const startTime = Date.now();
        
        const instructions = [
            { time: duration, text: 'Устройся поудобнее и закрой глаза...' },
            { time: duration - 30, text: 'Почувствуй свое дыхание...' },
            { time: duration - 60, text: 'Отпусти все мысли и тревоги...' },
            { time: duration - 120, text: 'Наслаждайся моментом покоя...' },
            { time: 30, text: 'Медленно готовься к завершению...' },
            { time: 10, text: 'Сделай последние глубокие вдохи...' }
        ];
        
        const countdown = setInterval(() => {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            timerDisplay.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            
            // Update instruction
            const currentInstruction = instructions.find(inst => timeLeft === inst.time);
            if (currentInstruction) {
                instruction.textContent = currentInstruction.text;
                this.showFloatingHearts(3);
            }
            
            if (timeLeft <= 0) {
                clearInterval(countdown);
                this.completeMeditation(duration);
                this.stopAmbientSound();
            }
            
            timeLeft--;
        }, 1000);
    }
    
    completeMeditation(duration) {
        const instruction = document.querySelector('.timer-instruction');
        const timerDisplay = document.querySelector('.timer-display');
        
        instruction.textContent = '✨ Медитация завершена! Отлично!';
        timerDisplay.textContent = '🧘‍♀️';
        
        // Update stats
        this.stats.totalTime += Math.floor(duration / 60);
        this.stats.sessionsCompleted += 1;
        
        // Check for achievements
        this.checkAchievements();
        
        // Show completion animation
        this.showCompletionAnimation('Медитация завершена!');
        
        this.saveUserData();
    }
    
    startBreathing() {
        const btn = document.getElementById('start-breathing');
        const guide = document.getElementById('breathing-guide');
        
        btn.style.display = 'none';
        guide.classList.remove('hidden');
        
        this.runBreathingExercise();
    }
    
    runBreathingExercise() {
        const instruction = document.querySelector('.breathing-instruction');
        const counter = document.querySelector('.breathing-counter');
        const circle = document.querySelector('.breathing-circle');
        
        let cycle = 1;
        const totalCycles = 4;
        
        const runCycle = () => {
            if (cycle > totalCycles) {
                instruction.textContent = '✨ Дыхательная практика завершена!';
                counter.textContent = 'Превосходно!';
                circle.style.animation = 'none';
                
                this.stats.totalTime += 5; // 5 minutes for breathing
                this.checkAchievements();
                this.saveUserData();
                return;
            }
            
            counter.textContent = `Цикл ${cycle} из ${totalCycles}`;
            
            // Inhale phase
            instruction.textContent = 'Глубокий вдох... (4 счета)';
            circle.style.animation = 'breatheIn 4s ease-in-out';
            
            setTimeout(() => {
                // Hold phase
                instruction.textContent = 'Задержи дыхание... (7 счетов)';
                circle.style.animation = 'breatheHold 7s ease-in-out';
                
                setTimeout(() => {
                    // Exhale phase
                    instruction.textContent = 'Медленный выдох... (8 счетов)';
                    circle.style.animation = 'breatheOut 8s ease-in-out';
                    
                    setTimeout(() => {
                        cycle++;
                        setTimeout(runCycle, 1000);
                    }, 8000);
                }, 7000);
            }, 4000);
        };
        
        runCycle();
    }
    
    playNatureSound(event) {
        const btn = event.target;
        const soundOption = btn.closest('.sound-option');
        const soundType = soundOption.dataset.sound;
        
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio = null;
        }
        
        // Mock audio playing with visual feedback
        btn.textContent = '⏸️ Остановить';
        btn.style.background = '#28a745';
        soundOption.style.borderColor = '#28a745';
        soundOption.style.boxShadow = '0 0 20px rgba(40, 167, 69, 0.3)';
        
        // In real app, this would load actual audio files
        const mockDuration = 30000; // 30 seconds
        
        setTimeout(() => {
            btn.textContent = 'Слушать';
            btn.style.background = '#6a5acd';
            soundOption.style.borderColor = 'transparent';
            soundOption.style.boxShadow = 'none';
            
            this.showAchievementNotification('🎵 Прослушал звуки природы');
        }, mockDuration);
        
        // Add some visual effects
        this.createSoundWaves(soundOption);
    }
    
    playAmbientSound(type) {
        // In real app, this would play actual meditation music
        console.log(`Playing ambient sound: ${type}`);
    }
    
    stopAmbientSound() {
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio = null;
        }
    }
    
    updateProgress() {
        const scrollPosition = window.scrollY;
        const documentHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercentage = Math.min((scrollPosition / documentHeight) * 100, 100);
        
        const progressBar = document.getElementById('progress');
        if (progressBar) {
            progressBar.style.width = scrollPercentage + '%';
        }
    }
    
    checkAchievements() {
        const newAchievements = [];
        
        // First meditation achievement
        if (this.stats.sessionsCompleted === 1 && !this.achievements.includes('first_meditation')) {
            newAchievements.push({
                id: 'first_meditation',
                title: '🧘‍♀️ Первая медитация',
                description: 'Поздравляем с первой практикой!'
            });
            this.achievements.push('first_meditation');
        }
        
        // Time-based achievements
        if (this.stats.totalTime >= 30 && !this.achievements.includes('meditation_novice')) {
            newAchievements.push({
                id: 'meditation_novice',
                title: '⏰ 30 минут практики',
                description: 'Отличное начало медитативного пути!'
            });
            this.achievements.push('meditation_novice');
        }
        
        // Show new achievements
        newAchievements.forEach(achievement => {
            this.showAchievementNotification(achievement.title, achievement.description);
        });
    }
    
    showAchievementNotification(title, description = '') {
        const notification = document.createElement('div');
        notification.className = 'achievement-notification';
        notification.innerHTML = `
            <div style="font-weight: bold; margin-bottom: 5px;">${title}</div>
            ${description ? `<div style="font-size: 0.9em; opacity: 0.8;">${description}</div>` : ''}
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 4000);
    }
    
    showFloatingHearts(count) {
        for (let i = 0; i < count; i++) {
            setTimeout(() => {
                const heart = document.createElement('div');
                heart.className = 'heart';
                heart.textContent = '💖';
                heart.style.left = Math.random() * window.innerWidth + 'px';
                heart.style.top = Math.random() * 100 + 'px';
                
                document.body.appendChild(heart);
                
                setTimeout(() => heart.remove(), 3000);
            }, i * 300);
        }
    }
    
    createSoundWaves(element) {
        // Visual effect for sound playing
        for (let i = 0; i < 3; i++) {
            setTimeout(() => {
                element.style.transform = `scale(${1 + i * 0.05})`;
                setTimeout(() => {
                    element.style.transform = 'scale(1)';
                }, 200);
            }, i * 400);
        }
    }
    
    showCompletionAnimation(message) {
        const overlay = document.createElement('div');
        overlay.className = 'lesson-complete-animation';
        overlay.innerHTML = `
            <div class="complete-content">
                <div class="complete-icon">🌟</div>
                <div class="complete-text">${message}</div>
                <div class="complete-subtitle">Ты сделал важный шаг к внутренней гармонии</div>
            </div>
        `;
        
        document.body.appendChild(overlay);
        
        setTimeout(() => {
            overlay.style.opacity = '0';
            setTimeout(() => overlay.remove(), 500);
        }, 2000);
    }
    
    completeLesson() {
        const lessonId = parseInt(document.body.dataset.lessonId) || 1;
        const completionTime = Math.floor((Date.now() - this.startTime) / 1000);
        
        // Send completion data to Telegram bot
        if (this.tg) {
            this.tg.sendData(JSON.stringify({
                action: 'lesson_complete',
                lesson_id: lessonId,
                completion_time: completionTime,
                stats: this.stats
            }));
            
            this.tg.close();
        } else {
            // Fallback for testing
            alert('Урок завершен! (В реальном боте откроется следующий этап)');
        }
    }
}

// CSS animations for breathing
const breathingStyles = `
@keyframes breatheIn {
    0% { transform: scale(1); background: radial-gradient(circle, #e8e6ff, transparent); }
    100% { transform: scale(1.3); background: radial-gradient(circle, #b8b5ff, transparent); }
}

@keyframes breatheHold {
    0%, 100% { transform: scale(1.3); background: radial-gradient(circle, #b8b5ff, transparent); }
}

@keyframes breatheOut {
    0% { transform: scale(1.3); background: radial-gradient(circle, #b8b5ff, transparent); }
    100% { transform: scale(1); background: radial-gradient(circle, #e8e6ff, transparent); }
}
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = breathingStyles;
document.head.appendChild(styleSheet);

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.meditationApp = new MeditationApp();
});