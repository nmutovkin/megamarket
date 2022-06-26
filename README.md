# MegaMarket Open API

![example workflow](https://github.com/nmutovkin/megamarket/actions/workflows/megamarket_workflow.yml/badge.svg)

MegaMarket - API веб-сервиса для анализа и сравнения цен на товары и различные категории товаров.
Сервис написан на Python с использованием Django и Django REST Framework.
Сервис доступен по ссылке https://experimental-1932.usr.yandex-academy.ru

## Документация

Документация API доступна по ссылке https://experimental-1932.usr.yandex-academy.ru/docs

## Локальный запуск проекта

1. Клонируем репозиторий на локальный компьютер
2. cd megamarket
3. [Опционально] Создаем и активируем виртуальное окружение python
4. Устанавливаем зависимости pip install -r requirements.txt
5. В корне проекта создаем файл с переменными окружения .env на базе .env.template
6. Применяем миграции python manage.py runserver
7. Запускаем сервер разработки python manage.py runserver

Сервис будет доступен на http://localhost:8000

## Краткое описание команд

1. /imports Добавить в базу набор товаров и категорий товаров
2. /nodes/{id} Показать информацию о товаре (или категории товаров) с индексом id, а также о дочерних товарах и категориях
3. /delete/{id} Удалить товар или категорию с индексом id и все дочерние элементы
4. /sales Показать информацию о товарах цена которых была обновлена за последние сутки
5. /node/{id}/statistic Информацию об истории обновления цены товара или категории с индексом id
