# Хранилища и базы данных

## Подготовка сервера

### Docker

https://docs.docker.com/engine/install/ubuntu/

### Oracle DB 

1. Скачать докер-образ https://yadi.sk/d/9nOqNSKgoRV5bA
1. Распаковать `unzip oracle_with_olaptrain.zip`
1. `docker load -i oracle_with_olaptrain.tar`
1. `docker run --name oracle -d -p 0.0.0.0:1521:1521 oracle_with_olaptrain`
1. `docker exec -ti -u oracle oracle bash`
1. В шелле делаем `sqlplus sys as sysdba@PDB1;`, пароль пустой. Затем выполняем последовательность команд:
```
shutdown;
startup;
ALTER PLUGGABLE DATABASE ALL OPEN;

alter session set container=pdb1;
create user lab_oracle_user identified by lab_oracle_user_password;
GRANT CONNECT,RESOURCE,DBA TO lab_oracle_user;
GRANT CREATE SESSION, GRANT ANY PRIVILEGE TO lab_oracle_user;
GRANT UNLIMITED TABLESPACE TO lab_oracle_user;

exit;
```
1. Выходим из шелла, Oracle DB готов и доступен на порту 1521.

### MySQL

1. `docker pull mysql`
1. `docker run --name mysql -e MYSQL_ROOT_PASSWORD=superstr0ngpassword -e MYSQL_USER=lab_mysql_user -e MYSQL_PASSWORD=lab_mysql_user_password -e MYSQL_DATABASE=lab -d -p 0.0.0.0:3306:3306 mysql`

Если контейнер тут же завершается, нужно подкрутить настройки у хоста: `sysctl -w fs.aio-max-nr=2097152`

### PostgreSQL

1. `docker pull postgres`
1. `docker run --name postgres -e POSTGRES_USER=lab_postgre_user -e POSTGRES_PASSWORD=lab_postgre_user_password -d -p 0.0.0.0:5432:5432 postgres:11`


### MongoDB

1. `docker pull mongo`
1. `docker run --name mongodb -e MONGO_INITDB_DATABASE=lab -e MONGO_INITDB_ROOT_USERNAME=lab_mongo_user -e MONGO_INITDB_ROOT_PASSWORD=lab_mongo_user_password -d -p 0.0.0.0:27017:27017 mongo`

## Подготовка клиента

1. Устанавливаем Python 3.6.x
2. Устанавливаем все пакеты из requirements.txt
3. Для Оракла накатываем библиотеки [по ссылке](https://oracle.github.io/odpi/doc/installation.html#oracle-instant-client-zip)
4. Для MySQL и PostgreSQL могут потребоваться дополнительные пакеты из пакетного менеджера вашей ОС

## Запуск

### Задание 1

Задание заключается в создании схемы в 4 БД и заполнении каждой БД своими данными. В `model/<database>` можно посмотреть объекты для конкретной базы данных.

Запуск из корня проекта: 
```
/usr/bin/python3 -m lab1 create
```

Повторный запуск удвоит количество записей во всех БД. Количество генерируемых записей можно изменять в функциях `fill_<database>` в `generator/<database>.py`

#### Схемы

Oracle:

![](./res/oracle.png)

PostgreSQL:

![](./res/postgres.png)

MySQL:

![](./res/mysql.png)

### Задание 2

Необходимо провести миграцию из четырёх БД в единую схему в Oracle DB. Объекты схемы можно найти в `model/final`.

Запуск из корня проекта: 
```
/usr/bin/python3 -m lab1 migrate
```

#### Схема

![](./res/final.png)

### Задание 3

#### Таблицы фактов

Перед началом работы нужно создать таблицы фактов. В данный момент они создаются в конце миграции.

FACT_2:

![](./res/fact_2.png)

**Примечание:** STREET_ID не может являться unique, так как данные хранятся в этой таблице, а не отдельной с улицами. Так сделано для удобства.


FACT_3:

![](./res/fact_3.png)

#### Установка Oracle Analytic Workspace Manager 

Необходимо получить из БД пару отчётов с помощью Oracle Analytic Workspace Manager.
Скачиваем [отсюда](https://www.oracle.com/database/technologies/olap-downloads.html) версию `for Oracle 12.1.0.2`.
Распаковываем, запускаем:
```
java -mx1024m -Duser.country=us -Duser.language=en -jar awm12.1.0.1.0B.jar
```

Подключаемся к нашей БД, создаём рабочее место аналитика. В качестве более подробного туториала можно опираться на [туториал от Оракла](https://www.oracle.com/ocom/groups/public/@otn/documents/webcontent/453094.htm).

#### Величины (Dimensions)

Элементы или объекты в логической схеме. В данном задании они заданы преподавателем и обозначены в [файле](./res/er-rus for awm.pdf). В нашем случае их четыре:

- место рождения (`birth_place`)
- место публикации (`publication_place`)
- время (`time`)
- общежитие (`dormitory`)

#### Уровни (Levels) и иерархии (Hierarchy)

Все данные можно группировать по различным критериям. Если грубо, то уровни и есть эти самые критерии. 
Проще всего это понять по времени. Данные со временем можно группировать по дням, неделям, месяцам, кварталам, года, etc. 
"День", "Неделя", "Месяц" -- это уровни
Последовательность "День -> Неделя -> Месяц" -- это иерархия, где "день" -- это наиболее низкий уровень, а "месяц" -- наиболее высокий.

Уровни и их иерархии так же заданы в [файле](./res/er-rus for awm.pdf). 

Вот они, для каждой величины от высокого к низкому уровню:
- место рождения (`birth_place`) 
    - все страны (`all_countries`)
    - страна (`country`)
    - город (`city`)
    - район (`district`)
- место публикации (`publication_place`)
    - все страны (`all_countries`)
    - страна (`country`)
    - город (`city`)
    - издание (`office`)
- время (`time`)
    - все года (`all_years`)
    - год (`year`)
    - семестр (`term`)
- общежитие (`dormitory`)
    - все общежития (`all_dormitories`)
    - общежитие (`dormitory`)
    
Заходим в маппинг величины и размечаем для каждого пункта свой столбец в таблице. Для наиболее высоких уровней оставляем строки. Например:
![](./res/mapping.png)

Так же AWM по имени `time` угадывает, что это будет дата/время. В этом типе данных нужно дополнить когда заканчивается промежуток и сколько "детей" может быть у уровня.

![](./res/mapping-time.png)

#### Кубы и отчёты

Кубы -- это представления данных на базе величин. Каждому кубу сопоставим свою таблицу фактов (по номеру).

- `LAB_CUBE_2`
    - Dimensions: `time`, `birth_place`
    - Measures: `TOTAL_PERSONS`
    - Calculated Measures: `None`
- `LAB_CUBE_3`
    - Dimensions: `time`, `pubication_place`
    - Measures: `TOTAL_PERSONS`
    - Calculated Measures: `None`

При создании куба во вкладке `Partitioning` убираем галку с пункта `Partition cube`.

После создания хотя бы одного измерения (Measures) можно размаппить куб на данные. 
Если информация обо всех уровнях иерархии хранится в одной таблице, достаточно указать ссылку на нижний уровень.

Так как мы считаем сумму людей, в верхней панельки в селекторе `Group By` оставляем `SUM`.

В отличие от маппинга уровней иерархии, здесь нужно прописать `Join Condition`, который связывает таблицу фактов и таблицу с информацией. Предполагается, что таблица фактов -- центр топологии "звезда" и Join можно прописать так: `<field1> = <field2>`.

Пример:

![](./res/cube-mapping.png)

Если всё сделано правильно, то ПКМ по кубу -> `Maintain Cube LAB_CUBE_2`. В появившемся диалоге можно смело нажимать `Finish` и ждать завершения обработки:

![](./res/maintenance-completed.png)

После этого можно смотреть данные в кубе. ПКМ по кубу -> `View Data LAB_CUBE_2...`

![](./res/measure-data-viewer-1.png)

![](./res/measure-data-viewer-2.png)


### Курсовая работа

Итоговый файл TableAU: [course_work.twb](./res/course_work.twb)

Курсовая работа -- продолжение ЛР1. Необходимо провести аналитику аналогичную третьему пункту ЛР1 на данных из второго пункта ЛР1.

Скачиваем [Tableau Desktop 2020 по студенчеству](https://www.tableau.com/academic/students). Необходимо приложить фотографию студенческого билета при регистрации. Ключ и ссылка на скачивание приходят достаточно быстро.

Установка тривиальна. Для подключения к Oracle DB нужен драйвер. Скачать можно [здесь](https://www.tableau.com/support/drivers): `Oracle - Windows - 64 bit`.

Подключаемся к базе данных и выбираем необходимые данные для нас. Мы будем играть в аналитика-библиотекаря, поэтому заводим только таблицы `F_PERSON` и `F_LIBRARY_RECORD`. 
Связывать с `F_TIME` не имеет смысла, так как ключ сам по себе является датой. 

![](./res/tableau-datasource.png)

Представим, что в нашей библиотеке два окна: по одному на приём и на выдачу книг. Хочется видеть сколько посетителей приходит в день в каждое окно и в какие дни библиотека наиболее популярна.

Построим по графику для каждого окна для отображения количества взятых в определённых день книг. По оси X даты, по Y -- количества.

![](./res/tableau-plot.png)

Сделаем красиво в заголовке сумму. Для этого создадим Calculated Measure. Количество сданных в аренду книг можно вычислить по количеству записей:
```
WINDOW_SUM(COUNT([F_LIBRARY_RECORD]))
```

С полученными сложнее. Их можно вычислить по null в RETURNED_AT. Воспользуемся этим:
```
WINDOW_SUM(SUM(IF ISNULL([RETURNED_AT_ID]) THEN 0 ELSE 1 END))
```

Так же добавим фильтр по дате, чтобы можно было менять временной промежуток.

В качестве полезного опыта построим таблицу с подсветкой:

![](./res/tableau-highlight-table.png)

Наиболее тёмные участки говорят о высокой популярности, светлые -- о низкой популярности.
Из этого графика видно, что даже синтетические данные, сгенерированные в ходе ЛР1 раскрывают суть студентов: пик посещаемости библиотек в октябре и декабре, то есть перед промежуточным контролём.

И под конец сделаем график с популряными книгами:

![](./res/tableau-books.png)

Все книги одинаково популярны. Но это скорее особенность генератора, нежели проблема аналитики. 

Создадим интерактивный дашбоард для руководителя библиотеки.

![](./res/tableau-dashboard.png)

Для создания хорошего дашбоарда надо причесать все имена осей, заголовки диаграмм и расставить фильтры. При перетаскивании на дашбоард за каждым графиком тянутся свои фильтры. Лишние можно удалить, а для оставшихся прописать, что фильтр регулирует не один график, а сразу всем:

![](./res/tableau-setup-filter.png)

После этого дашбоард готов к работе.