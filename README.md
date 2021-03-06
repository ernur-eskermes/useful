<h2 align="center">Useful</h2>


### Описание проекта:
Когда человек приходит в профессию программиста, чтобы научиться писать программы, нужно 
много практики и верная структура и последовательность в обучении, и командная разработка.
Чтобы научиться программировать, неопытных программистов отправляют найти проект на GitHub или написать свой проект. Но найти подходящий проект на GitHub молодому программисту тяжело, так как не реализован нужный поиск. 

Проект UseFul призван помочь таким людям.

### Инструменты разработки

**Стек:**
- Python >= 3.9
- FastAPI >= 0.68.1
- Tortoise ORM
- Postgres

## Старт

#### 1) Создать образ

    docker-compose build

##### 2) Запустить контейнер

    docker-compose up
    
##### 3) Перейти по адресу

    http://127.0.0.1:8000/docs

## Разработка с Docker

##### 1) Сделать форк репозитория

##### 2) Клонировать репозиторий

    git clone ссылка_сгенерированная_в_вашем_репозитории

##### 3) В корне проекта создать .env.dev

    SERVER_HOST=http://127.0.0.1:8000
    SECRET_KEY=fuf823rg2388gc828^&%&^%^&T^&gf

    # Data Base
    POSTGRES_DB=useful_dev
    POSTGRES_USER=useful_user
    POSTGRES_PASSWORD=useful_pass
    POSTGRES_HOST=useful-db
    
    # Email
    SMTP_TLS=True
    SMTP_PORT=587
    SMTP_HOST=smtp
    SMTP_USER=robot@your.com
    SMTP_PASSWORD=pass
    EMAILS_FROM_EMAIL=robot@your.com

    # GitHub 
    GITHUB_CLIENT_ID=example_client_id
    GITHUB_CLIENT_SECRET=example_client_secret


##### 4) Создать образ

    docker-compose build

##### 5) Запустить контейнер

    docker-compose up
    
##### 6) Создать миграции

    docker exec -it useful-back aerich init-db
    
##### 7) Создать суперюзера

    docker exec -it useful-back python scripts/createsuperuser.py

##### 8) Если не выполняет команды

- Войти в контейнер - _docker exec -it useful-back bash_
- Выполнить команды без _docker exec -it useful-back_ 
                                                        
##### 9) Если нужно очистить БД

    docker-compose down -v
 
##### 10) Создать миграции

    docker exec -it useful-back aerich migrate
 
##### 11) Выполнить миграции

    docker exec -it useful-back aerich upgrade
 
 
## License

[BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause)

Copyright (c) 2020-present, DJWOMS - Omelchenko Michael
