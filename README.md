# Django Money Tracker 💰

Веб-приложение для учета денежных операций с поддержкой категорий, подкатегорий, статусов и типов транзакций.

## 🚀 Возможности

- Добавление, редактирование и удаление транзакций
- Фильтрация по дате, категории, статусу, типу
- Каскадные категории и подкатегории
- Валидация логики транзакций
- Пагинация
- Поддержка нескольких валют и статусов

## 📦 Стек технологий

- Python 3.11
- Django 4.x
- Bootstrap 5
- SQLite (по умолчанию)
- AJAX (для динамической загрузки полей)

## 📂 Установка

```bash
git clone https://github.com/your-username/money-tracker.git
cd money-tracker
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
