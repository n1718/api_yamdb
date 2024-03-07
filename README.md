# Проект YaMDb
## Описание
Приложение для оценки различных произведений

Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором.

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.

Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

## Техническое описание проекта YaMDb

Для запуска проекта необходимо клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/RussianPostman/api_yamdb.git
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Импорт csv файлов:

```
python3 manage.py import_csv
```

Запустить проект:

```
python3 manage.py runserver
```

Перейти в браузере по адресу

```
http://127.0.0.1:8000
```

### Примеры запросов к API:

Получение списка всех категорий:

```
http://127.0.0.1:8000/api/v1/categories/
```
Получение списка всех жанров:

```
http://127.0.0.1:8000/api/v1/genres/
```

Получение списка всех произведений:

```
http://127.0.0.1:8000/api/v1/titles/
```

## Документация

К проекту по адресу
```
http://127.0.0.1:8000/redoc/
```
подключена документация API YaMDb. В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.

### Cписок используемых технологий:

- Django
- pytest
- djangorestframework
- djangorestframework-simplejwt

[Авторы проекта](https://static.sobaka.ru/images/image/01/62/43/08/_normal.png?v=1669034921):
Майстренко Мирослав,
Юрий Ожегов,
Дмитрий Денисенко.
