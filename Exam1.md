# Экзамен по Django REST Framework — Social Network API

 

## Модели проекта

1\. User

\- `username`, `first_name`, `last_name`, `age`, `created_at`

2\. Profile

\- `user`, `bio`, `city`, `birth_date`, `avatar`

3\. Post

\- `user`, `title`, `content`, `views`, `created_at`, `updated_at`

4\. Like

\- `user`, `post`, `created_at`

5\. Favorite

\- `user`, `post`, `created_at`

`User` — обычная модель без авторизации и входа в систему.

# Часть 1. User API  

### 1. Список пользователей

`GET /api/users/`

Вывести пользователей с количеством публикаций, поставленных лайков и избранных публикаций.

Пример JSON:

```
[
  {
    "id": 1,
    "username": "ali",
    "full_name": "Ali Karimov",
    "age": 19,
    "posts_count": 12,
    "likes_count": 35,
    "favorites_count": 8
  },
  {
    "id": 2,
    "username": "farid",
    "full_name": "Farid Rahimov",
    "age": 20,
    "posts_count": 5,
    "likes_count": 14,
    "favorites_count": 3
  }
]
```

### 2. Детали пользователя

`GET /api/users/1/`

Вывести информацию о пользователе, его профиль и статистику публикаций.

```
{
  "id": 1,
  "username": "ali",
  "full_name": "Ali Karimov",
  "age": 19,
  "profile": {
    "bio": "Python developer",
    "city": "Khujand"
  },
  "statistics": {
    "posts_count": 12,
    "total_views": 5400,
    "likes_received": 95,
    "favorites_received": 30
  }
}
```

### 3. CRUD пользователей

- `POST /api/users/` — создать пользователя.
- `PUT /api/users/1/` — полностью обновить пользователя.
- `PATCH /api/users/1/` — частично обновить пользователя.
- `DELETE /api/users/1/` — удалить пользователя.

Пример создания:

```
{
  "username": "muhammad",
  "first_name": "Muhammad",
  "last_name": "Saidov",
  "age": 21
}
```

### 4. Самые активные пользователи

`GET /api/users/most-active/`

Вывести 10 пользователей с наибольшим количеством публикаций.

```
[
  {
    "id": 1,
    "username": "ali",
    "posts_count": 12
  },
  {
    "id": 2,
    "username": "farid",
    "posts_count": 10
  }
]
```

### 5. Статистика пользователей

`GET /api/users/statistics/`

Вывести общее количество пользователей, средний возраст, минимальный и максимальный возраст.

```
{
  "total_users": 100,
  "average_age": 22.4,
  "min_age": 16,
  "max_age": 35
}
```

# Часть 2. Profile API  

### 6. Список профилей

`GET /api/profiles/`

Вывести профили вместе с информацией о владельце и количеством его публикаций.

```
[
  {
    "id": 1,
    "user": {
      "id": 1,
      "username": "ali",
      "full_name": "Ali Karimov"
    },
    "bio": "Backend developer",
    "city": "Khujand",
    "posts_count": 12
  }
]
```

### 7. CRUD профилей

- `GET /api/profiles/1/` — получить профиль.
- `POST /api/profiles/` — создать профиль.
- `PUT /api/profiles/1/` — полностью обновить профиль.
- `PATCH /api/profiles/1/` — частично обновить профиль.
- `DELETE /api/profiles/1/` — удалить профиль.

Пример создания:

```
{
  "user": 1,
  "bio": "Python developer",
  "city": "Khujand",
  "birth_date": "2005-02-23"
}
```

### 8. Статистика по городам

`GET /api/profiles/city-statistics/`

Вывести количество пользователей в каждом городе.

```
[
  {
    "city": "Khujand",
    "users_count": 40
  },
  {
    "city": "Dushanbe",
    "users_count": 35
  },
  {
    "city": "Bokhtar",
    "users_count": 10
  }
]
```

# Часть 3. Post API  

### 9. Список публикаций

`GET /api/posts/`

Вывести публикации с данными автора, количеством лайков, избранного и признаком популярности.

```
[
  {
    "id": 1,
    "title": "Django ORM",
    "content": "Learning annotate and aggregate",
    "author": {
      "id": 1,
      "username": "ali",
      "full_name": "Ali Karimov"
    },
    "views": 1500,
    "likes_count": 12,
    "favorites_count": 4,
    "is_popular": true,
    "created_at": "2026-10-10T10:00:00Z"
  }
]
```

### 10. Детали публикации

`GET /api/posts/1/`

Вывести публикацию, автора, пользователей, поставивших лайки, и пользователей, добавивших её в избранное.

```
{
  "id": 1,
  "title": "Django ORM",
  "content": "Learning annotate and aggregate",
  "author": {
    "id": 1,
    "username": "ali"
  },
  "views": 1500,
  "likes_count": 12,
  "favorites_count": 4,
  "liked_by": [
    {
      "id": 2,
      "username": "farid"
    },
    {
      "id": 3,
      "username": "muhammad"
    }
  ],
  "favorited_by": [
    {
      "id": 2,
      "username": "farid"
    }
  ],
  "is_popular": true,
  "is_viral": true,
  "status": "has_likes"
}
```

### 11. CRUD публикаций

- `POST /api/posts/` — создать публикацию.
- `PUT /api/posts/1/` — полностью обновить публикацию.
- `PATCH /api/posts/1/` — частично обновить публикацию.
- `DELETE /api/posts/1/` — удалить публикацию.

Пример создания:

```
{
  "user": 1,
  "title": "My first post",
  "content": "Learning Django REST Framework",
  "views": 0
}
```

### 12. Публикации конкретного пользователя

`GET /api/users/1/posts/`

Вывести все публикации пользователя и количество его публикаций.

```
{
  "user": {
    "id": 1,
    "username": "ali"
  },
  "posts_count": 2,
  "results": [
    {
      "id": 1,
      "title": "Django ORM",
      "likes_count": 12,
      "views": 1500
    },
    {
      "id": 2,
      "title": "DRF Serializers",
      "likes_count": 8,
      "views": 900
    }
  ]
}
```

### 13. Популярные публикации

`GET /api/posts/popular/`

Вывести публикации, у которых не менее 10 лайков, отсортированные по количеству лайков в порядке убывания.

```
[
  {
    "id": 1,
    "title": "Django ORM",
    "likes_count": 120,
    "favorites_count": 80,
    "is_popular": true
  },
  {
    "id": 5,
    "title": "Python Tips",
    "likes_count": 95,
    "favorites_count": 55,
    "is_popular": true
  }
]
```

### 14. Поиск и фильтрация публикаций

`GET /api/posts/search/?q=django`

Искать публикации по заголовку и содержимому.

`GET /api/posts/filter/?min_views=100&max_views=2000&user_id=1`

Фильтровать публикации по автору и диапазону просмотров.

Пример JSON:

```
[
  {
    "id": 1,
    "title": "Django ORM",
    "views": 1500,
    "likes_count": 12
  },
  {
    "id": 2,
    "title": "Django REST Framework",
    "views": 900,
    "likes_count": 8
  }
]
```

### 15. Статистика публикаций

`GET /api/posts/statistics/`

Вывести общее количество публикаций, просмотров, среднее количество просмотров, максимальное и минимальное количество просмотров, общее количество лайков и избранного.

```
{
  "total_posts": 250,
  "total_views": 112625,
  "average_views": 450.5,
  "max_views": 5000,
  "min_views": 0,
  "total_likes": 1200,
  "total_favorites": 450
}
```

### 16. Статистика публикаций по авторам

`GET /api/posts/author-statistics/`

Для каждого автора вывести количество публикаций, общие и средние просмотры, количество полученных лайков.

```
[
  {
    "user_id": 1,
    "username": "ali",
    "posts_count": 12,
    "total_views": 5400,
    "average_views": 450,
    "likes_received": 95
  },
  {
    "user_id": 2,
    "username": "farid",
    "posts_count": 5,
    "total_views": 2100,
    "average_views": 420,
    "likes_received": 30
  }
]
```

# Часть 4. Like API  

### 17. Список лайков

`GET /api/likes/`

Вывести лайки с информацией о пользователе и публикации.

```
[
  {
    "id": 1,
    "user": {
      "id": 2,
      "username": "farid"
    },
    "post": {
      "id": 1,
      "title": "Django ORM"
    },
    "created_at": "2026-10-10T10:30:00Z"
  }
]
```

### 18. Создание и удаление лайка

- `POST /api/likes/` — поставить лайк.
- `DELETE /api/likes/1/` — удалить лайк.

Пример создания:

```
{
  "user": 2,
  "post": 1
}
```

Один пользователь не может поставить несколько лайков одной публикации. При повторной попытке вернуть понятную ошибку.

### 19. Лайки конкретной публикации

`GET /api/posts/1/likes/`

Вывести список пользователей, поставивших лайки, и общее количество лайков.

```
{
  "post_id": 1,
  "likes_count": 12,
  "users": [
    {
      "id": 2,
      "username": "farid"
    },
    {
      "id": 3,
      "username": "muhammad"
    }
  ]
}
```

### 20. Рейтинг публикаций по лайкам

`GET /api/likes/top-posts/`

Вывести 10 публикаций с наибольшим количеством лайков.

```
[
  {
    "post_id": 1,
    "title": "Django ORM",
    "likes_count": 120
  },
  {
    "post_id": 5,
    "title": "Python Tips",
    "likes_count": 95
  }
]
```

# Часть 5. Favorite API  

### 21. Список избранного

`GET /api/favorites/`

Вывести список избранного с информацией о пользователе, публикации, авторе публикации и количестве лайков.

```
[
  {
    "id": 1,
    "user": {
      "id": 2,
      "username": "farid"
    },
    "post": {
      "id": 1,
      "title": "Django ORM",
      "author": "ali",
      "likes_count": 12
    },
    "created_at": "2026-10-10T11:00:00Z"
  }
]
```

### 22. Добавление и удаление избранного

- `POST /api/favorites/` — добавить публикацию в избранное.
- `DELETE /api/favorites/1/` — удалить из избранного.

Пример создания:

```
{
  "user": 2,
  "post": 1
}
```

Один пользователь не может добавить одну публикацию в избранное несколько раз. При повторной попытке вернуть понятную ошибку.

### 23. Избранное конкретного пользователя

`GET /api/users/2/favorites/`

Вывести все сохранённые публикации пользователя, количество лайков и просмотров каждой публикации.

```
{
  "user": "farid",
  "favorites_count": 2,
  "results": [
    {
      "post_id": 1,
      "title": "Django ORM",
      "likes_count": 12,
      "views": 1500
    },
    {
      "post_id": 5,
      "title": "Python Tips",
      "likes_count": 95,
      "views": 3200
    }
  ]
}
```

# Часть 6. Комплексная аналитика  

### 24. Аналитика пользователя

`GET /api/users/1/analytics/`

Вывести статистику публикаций пользователя, просмотров, полученных и поставленных лайков, избранного и активности за последние 7 дней.

```
{
  "user": {
    "id": 1,
    "username": "ali",
    "full_name": "Ali Karimov"
  },
  "posts": {
    "posts_count": 12,
    "total_views": 5400,
    "average_views": 450
  },
  "engagement": {
    "likes_received": 95,
    "favorites_received": 30,
    "likes_given": 35,
    "favorites_given": 8
  },
  "activity": {
    "posts_last_7_days": 3,
    "is_active_user": true
  }
}
```

### 25. Главная страница и общая статистика

`GET /api/dashboard/`

Вывести общую статистику социальной сети, самого активного пользователя, самую популярную публикацию и последние 5 публикаций.

```
{
  "statistics": {
    "users_count": 100,
    "profiles_count": 85,
    "posts_count": 250,
    "likes_count": 1200,
    "favorites_count": 450,
    "total_views": 112625,
    "average_views": 450.5
  },
  "most_active_user": {
    "id": 1,
    "username": "ali",
    "posts_count": 12
  },
  "most_popular_post": {
    "id": 1,
    "title": "Django ORM",
    "likes_count": 120
  },
  "latest_posts": [
    {
      "id": 10,
      "title": "DRF Practice",
      "author": "farid",
      "likes_count": 5
    },
    {
      "id": 11,
      "title": "Python Tips",
      "author": "muhammad",
      "likes_count": 8
    }
  ]
}
```
 