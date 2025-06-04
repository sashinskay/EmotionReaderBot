# Emotion Analysis Telegram Bot

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.x-green.svg)](https://docs.aiogram.dev/)

Бот для анализа эмоциональной окраски текста с использованием нейросетевой модели.

## 📌 Основные функции
- Определение тональности текста (POSITIVE/NEGATIVE/NEUTRAL)
- Два формата ответа: текстовый и с GIF-анимациями
- Интерактивное меню с кнопками
- Поддержка многопользовательского режима

## 🛠 Технологический стек
- **Модель**: `rubert-base-cased-sentiment` (HuggingFace)
- **Бэкенд**: FastAPI
- **Бот**: Aiogram 3.x
- **Деплой**: Docker + Heroku

## Структура проекта
emotion-bot/
- ├── bot.py                # Основной код Telegram бота
- ├── app.py                # FastAPI сервер для обработки текста
- ├── requirements.txt      # Зависимости Python

## 🚀 Установка и запуск

1. Клонировать репозиторий:
```bash
git clone https://github.com/sashinskay/EmotionReaderBot.git
cd EmotionReaderBot/EmotionReaderBot
