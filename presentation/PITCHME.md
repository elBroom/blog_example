#HSLIDE
# Metareport

#HSLIDE
### Зачем?
Для получения более детальной информации по кампаниям в AdFox

По сути это выборка по логам AdFox

#HSLIDE
### Используемые технологии
- ClickHouse
- PostgreSQL
- Python 3.5
- flask
- celery

#HSLIDE
### Как это работает?

#HSLIDE
<img src="presentation/assets/img/howWork.jpg" alt="howWork"/>

#HSLIDE
### Агрегация

#HSLIDE
### Команда для агрегации
```
$ python manage.py aggregator adfox 2017_01_01_*
```

#HSLIDE
### Логи AdFox
[Документация](https://sites.help.adfox.ru/page/150/) по логам

Для кампаний по умолчанию поле `campaign_id` и `banner_id` равны нулю

Поля `ocN` это пользовательские таргетинги
- `oc6` - по позиции в блоке
- `oc10` - по жанрам
- `oc24` - по вендорам SmartTV
- `oc30` - позиция

[Подробнее](https://login.adfox.ru/page/userCriterias.php)

#HSLIDE
AdFox может перевыложить логи задним числом.

В CH данные можно только вставлять. Что бы "обновить" данные используется движок таблицы `CollapsingMergeTree` и поле таблицы `sign`.

#HSLIDE
<img src="presentation/assets/img/CollapsingMerge.jpg" alt="CollapsingMerge"/>

#HSLIDE
### Загрузка логов AdFox в ClickHouse
1. Поиск файла для агрегации по заданному паттерну
1. Получение файлов которые не были еще агрегированы
1. Создание таблицы для обновленных данных
1. Загрузка данных из основной таблицу в таблицу для обновленных данных со знаком -1
1. Создание таблицы для сырых данных
1. Загрузка новых данных в таблицу
1. Агрегация сырых данных со знаком 1 в таблицу для обновленных данных. Группировка по полям которые не участвуют в метрике.
1. Перенос данных в основную таблцу
1. Удаление всех вспамогательных таблиц
1. Помечаем файл как агрегированых

@see aggregator/aggregator.py:aggregate


#HSLIDE
### Доступ к логам

#HSLIDE
запрос на получение отчета по группе разделов для ivi
```
POST /api/reports
{
    "start_date": "2016-08-01",
    "end_date": "2016-08-01",
    "metrics": ["impressions"],
    "dimensions": ["campaign_id", "day", "cpm", "section_group"],
    "order_by": ["campaign_id", "day"],
    "conditions": [
        {
            "key": "site_id",
            "values": [31322],
            "equals": true
        },
        {
            "key": "campaign_id",
            "values": [0],
            "equals": false
        },
        {
            "key": "section_id",
            "values": [63675, 63671, 63661, 63648, 63682, 63637, 63619, 63623, 67503, 88052, 88051, 88050, 88049, 88048, 88047, 88046, 88044, 88043],
            "equals": true
        }
    ]
}
```

#HSLIDE
```
{
    "data": {
        ...
        "id": "75c13138-0a01-4324-98f3-6d8dc343ff69",
        "link": "75c13138-0a01-4324-98f3-6d8dc343ff69.tsv",
        "status": "ADDED"
    },
    "status": 200
}
```

#HSLIDE
Веб приложение формирует задачу для celery и сохраняет мета информацию об отчете в БД.

@see web/report.py:add_reports

celery задача генерирует и отправляет SQL запрос в ClickHouse через `clickhouse-client`. Результат запроса сохраняется в формате tsv с помощью CH.

@see web/tasks.py:generate_report_task

#HSLIDE
### Метрики
Это аддитивная величина

Для нее нужно учитывать `sign`

@see web/sql.py:known_metrics


#HSLIDE
### Измерения
Поля по которым идет группировка

В CH измерения храняться в виде id, для человекочитаемого вида используются словари.

@see web/sql.py:known_dimensions

#HSLIDE
### Словари в ClickHouse
[Документация](https://clickhouse.yandex/reference_ru.html#Внешние словари)

Запуск генерации "Конфигурационного файла для словаря"
```
$ python manage.py dictinary_generator
```

@see dictionary_generator.py:generate

данные в для словаря формируются на стороне ITD в файл tsv (id, name) и далее тянуться в metareport

#HSLIDE
### Сортировка
Название полей из метрик и измерений

#HSLIDE
### Условия
```
{
    "key": "campaign_id",
    "values": [0],
    "equals": false
},
```
@see web/sql.py:known_conditions_set
Сейчас поддерживаются только целочисленные значения

#HSLIDE
### Особенности ClickHouse
- тип колонки нужно приводить явно `toInt8(1)`
- время храниться в соответствии с часовым поясом на сервере. Сейчас сервер настроен на UTC, CH настроен на московское время.

#HSLIDE
### получение статуса отчета
```
GET /api/reports/75c13138-0a01-4324-98f3-6d8dc343ff69
```

#HSLIDE
### Вопросы?

#HSLIDE
### Спасибо за внимание