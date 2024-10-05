# Yamdb
## Описание проекта:
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Стек:
* python3.9
* Django 3.2
* DRF 3.12.4
* djangorestframework-simplejwt 5.3.1
* PyJWT 2.5.0

## Установка и запуск проекта:
* Клонировать репозиторий и перейти в диреткорию проекта:
```bash
git clone https://github.com/AlexandrYakhlakov/api_yamdb.git && cd api_yamdb 
```
* Cоздать и активировать виртуальное окружение:
```bash
python -m venv venv
```
```bash
source venv/bin/activate
```
* Установить зависимости из requirements.txt:
```
pip install -r requirements.txt
```
*  Перейти в директорию django проекта
```bash
cd api_yamdb
```
* Применить миграции:
```bash
python manage.py migrate
```
* Запуск
```bash
python manage.py runserver
```

## API документация: http://127.0.0.1:8000/redoc/

## Функциональности проекта:
* Админ панель: http://127.0.0.1:8000/admin/
* Регистрация и аутентификация
* Выдача JWT-токена пользователю
* Обновление кодов подтверждения
* Отправка кодов подтверждения по email(письма сохраняются в директории api_yamdb/sent_emails)
* Взаимодействие с категориями произведений
* Взаимодействие с жанрами произведений
* Взаимодействие с произведениями
* Взаимодействие с отзывами к произведению
* Взаимодействие с комментариями к отзыву
* Взаимодействие с учетными записями пользователей
