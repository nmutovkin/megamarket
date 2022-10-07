# MegaMarket Open API

![example workflow](https://github.com/nmutovkin/megamarket/actions/workflows/megamarket_workflow.yml/badge.svg)

MegaMarket - API веб-сервиса для анализа и сравнения цен на товары и различные категории товаров.

# Технологии
* Python
* Django
* Django REST Framework
* Docker

## Локальный запуск проекта

* Клонируем репозиторий на локальный компьютер ```git clone https://github.com/nmutovkin/megamarket.git```
* ```cd megamarket```
* Создаем и активируем виртуальное окружение python
    ```
    python -m venv venv
    source venv/bin/activate
    ```
* Устанавливаем зависимости ```pip install -r requirements.txt```
* В корне проекта создаем файл с переменными окружения ```.env``` на базе ```.env.template```
* Применяем миграции ```python manage.py migrate```
* Запускаем сервер разработки ```python manage.py runserver```

Сервис будет доступен на ```http://localhost:8000```
Документация API доступна по ссылке ```http://localhost:8000/docs```

## Краткое описание API запросов

1. ```/imports``` Добавить в базу набор товаров и категорий товаров
2. ```/nodes/{id}``` Показать информацию о товаре (или категории товаров) с индексом id, а также о дочерних товарах и категориях
3. ```/delete/{id}``` Удалить товар или категорию с индексом id и все дочерние элементы
4. ```/sales``` Показать информацию о товарах цена которых была обновлена за последние сутки
5. ```/node/{id}/statistic``` Информация об истории обновления цены товара или категории с индексом id

# Автор

Никита Мутовкин
