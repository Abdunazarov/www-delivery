# Приложение Доставки (WWW Delivery)

## Обзор

Данное приложение доставки представляет собой современное решение для управления процессами доставки товаров. Оно включает в себя функциональность для создания посылок, расчета стоимости доставки, управления типами посылок и получения информации о посылках. Разработанное с использованием FastAPI, приложение обеспечивает высокую производительность и легкость интеграции.

### Основные возможности

- **Асинхронное API**: Приложение использует асинхронные запросы, обеспечивая быструю обработку данных.
- ** Масштабируемость**: Использование Docker позволяет нам легко масштабировать приложение и добавлять новые сервисы.
- **Расчет стоимости доставки**: Возможность асинхронного расчета стоимости доставки с помощью задач Celery.
- **Документация API с Swagger**: Автоматически генерируемая документация API, доступная через Swagger UI.

### Технологический стек

- FastAPI
- SQLAlchemy (асинхронный интерфейс)
- PostgreSQL
- Celery для асинхронных задач
- Docker и Docker Compose для развертывания

## Как запустить

Для запуска приложения вам потребуется Docker и Docker Compose. Инструкции ниже предполагают, что эти инструменты уже установлены на вашем компьютере.

### Клонирование репозитория

Сначала клонируйте репозиторий на ваш локальный компьютер:

```bash
git clone https://github.com/Abdunazarov/www-delivery.git
cd www-delivery
```

### Запуск с помощью Docker Compose

Для запуска приложения и всех зависимых сервисов (база данных, Redis и т.д.) используйте Docker Compose:

```bash
docker-compose up --build
```

После успешного запуска приложение будет доступно на `http://localhost:8000`, а документация API - на `http://localhost:8000/docs`.

### Использование приложения

#### Создание посылки

Чтобы создать новую посылку, отправьте POST-запрос на `/parcels` с необходимыми данными о посылке.

#### Получение информации о посылках

- Получить список всех посылок: отправьте GET-запрос на `/parcels`.
- Получить информацию о конкретной посылке: отправьте GET-запрос на `/parcels/{parcel_id}`, где `{parcel_id}` - идентификатор посылки.

#### Расчет стоимости доставки

Отправьте POST-запрос на `/parcels/calculate-delivery-cost` для запуска задачи расчета стоимости доставки.