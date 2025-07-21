# LMS API

💼 Backend-система для управления онлайн-курсами, реализованная на Django + DRF с JWT-авторизацией, правами доступа, Docker и Celery.

---

## 🚀 Основной функционал

- JWT-аутентификация (`djangorestframework-simplejwt`)
- Кастомная модель пользователя (`CustomUser`)
- Регистрация и управление пользователями
- CRUD для курсов и уроков
- Роли: модераторы и владельцы объектов
- Разграничение доступа к профилям
- Подписка на курсы
- Celery + Redis для фоновых задач

---

## 🔐 Аутентификация

### Получение токенов:
`POST /api/token/`  
```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

### Обновление access-токена:
`POST /api/token/refresh/`  
```json
{
  "refresh": "your_refresh_token"
}
```

---

## 👤 Пользователи

### Регистрация:
`POST /api/users/register/`  
```json
{
  "email": "new@example.com",
  "username": "nickname",
  "password": "123456"
}
```

### Получение профиля:
- `GET /api/users/<id>/` — ограниченный доступ
- `PUT /api/users/<id>/` — только владелец

---

## 🎓 Курсы

- `GET /courses/` — список курсов
- `POST /courses/` — создать (владелец)
- `GET /courses/<id>/` — детали
- `PUT /courses/<id>/` — изменить (владелец или модератор)
- `DELETE /courses/<id>/` — удалить (только владелец)

---

## 📚 Уроки

- `GET /courses/<course_id>/lessons/` — уроки курса
- `POST /courses/<course_id>/lessons/` — создать урок
- `GET /lessons/<id>/` — детали
- `PUT /lessons/<id>/` — редактирование (владелец/модератор)
- `DELETE /lessons/<id>/` — только владелец

---

## 🔐 Права и роли

### Модераторы:
- Задают через админку (`auth.group`)
- Могут редактировать чужие курсы и уроки
- Не могут удалять или создавать

### Владельцы:
- Полный доступ к своим объектам

---

## 🔧 Пермишены

| Permission        | Описание                                         |
|------------------|--------------------------------------------------|
| `IsAuthenticated`| Только авторизованные пользователи               |
| `IsModerator`    | Пользователь в группе `Moderators`               |
| `IsOwner`        | Владелец объекта                                  |
| `IsSelf`         | Просмотр своего профиля                           |

---

## ⚙️ Установка без Docker

```bash
poetry install
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata users/fixtures/groups.json
python manage.py runserver
```

---

## 🐳 Docker-версия

### Шаги запуска:

```bash
# Собрать и запустить все сервисы
docker-compose up --build
```

### Сервисы:

| Сервис        | Назначение                      | Проверка                                 |
|---------------|----------------------------------|-------------------------------------------|
| `web`         | Django API (`localhost:8000`)   | http://localhost:8000                     |
| `db`          | PostgreSQL                      | pgAdmin / `docker exec -it postgres psql` |
| `redis`       | Хранилище Celery                | —                                         |
| `celery`      | Фоновый воркер                  | Логи: `docker logs celery`                |
| `celery_beat` | Планировщик задач               | Логи: `docker logs celery_beat`           |

---

## 🧪 Тестирование

```bash
pytest
```

Все ограничения проверены вручную через Postman:

- Только владельцы — CRUD своих объектов
- Модераторы — чтение и изменение чужих
- Нельзя просматривать чужие email и личные данные

---

## 📁 Структура проекта

```
LMS/
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   ├── urls.py
│   └── fixtures/
│       └── groups.json
├── courses/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── Dockerfile
├── docker-compose.yaml
├── .env.example
└── README.md
```

---

## 🌐 Переменные окружения (`.env.example`)

```env
SECRET_KEY=
DEBUG=
DJANGO_SETTINGS_MODULE=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
DATABASE_URL=
REDIS_URL=
```

```bash
python manage.py dumpdata auth.group --indent 2 > users/fixtures/groups.json
```

- В проекте используется `Poetry`, `Docker`, `Celery`, `PostgreSQL`, `Redis`

---

## CI/CD

В проекте используется GitHub Actions.

### Запуск CI

CI автоматически запускается при каждом push и pull request. В пайплайне:

- Проверка кода через flake8
- Прогон всех миграций
- Юнит-тесты

### Secrets

Для корректной работы настроены следующие GitHub Secrets:

- `ENV_FILE` — содержимое .env для CI

---

