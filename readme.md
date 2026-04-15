# Team Finder

Веб-приложение для поиска команды на проекты. Пользователи могут создавать проекты, находить участников и вступать в чужие команды.

## Возможности

- Регистрация и аутентификация по email
- Создание и редактирование проектов
- Поиск участников по навыкам
- Система избранных проектов
- Автоматическая генерация аватаров

## Стек

- **Backend**: Python 3.13, Django 5.2
- **База данных**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript
- **Изображения**: Pillow

## Установка

### 1. Клонировать репозиторий

```bash
git clone https://github.com/kvydev/team-finder-ad.git
cd team-finder
```

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
.venv\Scripts\activate          # Windows
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Настроить переменные окружения

```bash
cp .env_example .env
```

Заполнить `.env`:

```env
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True

POSTGRES_DB=team_finder
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 5. Применить миграции

```bash
python manage.py migrate
```

### 6. Создать суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Запустить сервер

```bash
python manage.py runserver
```

Приложение будет доступно по адресу `http://127.0.0.1:8000/`

## Структура проекта

```
team_finder/       # настройки Django
users/             # приложение пользователей
projects/          # приложение проектов
templates/         # HTML-шаблоны
static/            # CSS, JS, изображения
constants/         # константы проекта
```

## Административная панель

Доступна по адресу `/admin/` для пользователей с флагом `is_staff=True`.