````markdown
# LMS API

💼 Backend-система для управления онлайн-курсами, реализованная на Django + DRF с JWT-авторизацией и разграничением прав доступа.

## 🚀 Основной функционал

- JWT-аутентификация (`djangorestframework-simplejwt`)
- Кастомная модель пользователя (`CustomUser`)
- Регистрация пользователей
- CRUD для курсов и уроков
- Групповые права: `Moderators`
- Пермишены: только владельцы могут управлять своими объектами, модераторы — только читать/редактировать
- Безопасный просмотр профилей: только часть информации доступна другим

---

## 🔐 Аутентификация

### Получение токенов:
`POST /api/token/`  
```json
{
  "email": "user@example.com",
  "password": "your_password"
}
````

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

* `GET /api/users/<id>/` — любой пользователь, но видимость ограничена
* `PUT /api/users/<id>/` — только владелец

---

## 🎓 Курсы

* `GET /courses/` — список курсов
* `POST /courses/` — создать (только автор)
* `GET /courses/<id>/` — детали
* `PUT /courses/<id>/` — изменить (владелец или модератор)
* `DELETE /courses/<id>/` — удалить (только владелец)

---

## 📚 Уроки

* `GET /courses/<course_id>/lessons/` — уроки курса
* `POST /courses/<course_id>/lessons/` — создать урок
* `GET /lessons/<id>/` — детали
* `PUT /lessons/<id>/` — редактирование (владелец или модератор)
* `DELETE /lessons/<id>/` — только владелец

---

## 🔐 Права и роли

### Модераторы:

* Назначаются через админку (группа: `Moderators`)
* Могут просматривать и редактировать **любые** курсы и уроки
* Не могут создавать или удалять курсы и уроки

### Владельцы:

* Могут создавать, редактировать и удалять **только свои** объекты

---

## Пермишены

| Permission        | Описание                                         |
| ----------------- | ------------------------------------------------ |
| `IsAuthenticated` | Авторизованные пользователи                      |
| `IsModerator`     | Пользователь в группе `Moderators`               |
| `IsOwner`         | Пользователь — владелец объекта                  |
| `IsSelf`          | Пользователь — владелец просматриваемого профиля |

---

## ⚙️ Установка и запуск

```bash
poetry install
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata users/fixtures/groups.json
python manage.py runserver
```

---

##  Тестирование доступа

 Все ограничения проверены через Postman:

* Модераторы видят и редактируют чужое
* Владельцы работают только со своими
* Регистрация и JWT — открыты
* Профили — защищены

---

## 📁 Структура проекта

```
LMS/
├── users/
│   ├── models.py         # CustomUser, Payment
│   ├── permissions.py    # IsModerator, IsOwner, IsSelf
│   ├── serializers.py    # Public/PrivateUserSerializer
│   ├── views.py          # Регистрация, профиль
│   └── urls.py
├── courses/
│   ├── models.py         # Course, Lesson
│   ├── views.py          # ViewSet'ы с правами
│   ├── serializers.py
│   └── urls.py
├── users/fixtures/groups.json  # группа Moderators
└── manage.py
```

---

##  Примечания

* Создание групп через фикстуру:
  `python manage.py dumpdata auth.group --indent 2 > users/fixtures/groups.json`

* JWT настроен через `djangorestframework-simplejwt`

---
