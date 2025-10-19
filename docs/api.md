# Habits API Documentation

## Обзор

API для трекинга привычек с интеграцией Telegram для напоминаний.

## Базовый URL
http://localhost:8000/api/

## Аутентификация

Используется JWT (JSON Web Token) аутентификация.

### Регистрация

**POST** `/register/`

```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "telegram_chat_id": 123456789
}