# FromExcelTGSender

## Описание
Бот, который рассылает сообщения по чатам по списку задач из Гугл таблицы (по расписанию)

## Запуск
```bash
cp .env.example .env
```

Впишите необходимые данные в переменные окружения:
```env
SPREADSHEET_ID= # айди таблицы, с которой будем работать
BOT_TOKEN=
MAIN_WORK_SHEET_ID= # айди главной страницы
```

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

```bash
nano keys.json
```
Вставляем в *keys.json* ключи от Google API.

Так же в таблице необходимо раздать доступ гугл сервису, через который будет работать наш скрипт (редактор).

## Структура
 - [main](main.py) - инициализация проекта, цикла проверки таблицы на новые сообщения
 - [Model](Model.py) - модель сообщений (pydantic), валидаторы
 - [GoogleSheets](GoogleSheets.py) - работа с гугл таблицами, получение неотправленных сообщений, пометка отпралвенных
 - [Bot](Bot.py) - отправка сообщений
 - 
## Пример работы
 - Создаём таблицу
![screenshot](https://i.ibb.co/gb7CSXgD/Screenshot-From-2025-03-16-17-26-29.png)
 - Запускаем наш скрипт
 - Видим в терминале `2025-03-16T16:52:30.081018+0300 INFO 5 new messages`
 - Получаем сообщения

![screenshot](https://i.ibb.co/Lz8RFPhR/Screenshot-From-2025-03-16-17-29-48.png)

![screenshot](https://i.ibb.co/Jw8RwPcx/Screenshot-From-2025-03-16-17-31-03.png)

 - Таблица будет автоматически отредактирована:

![screenshot](https://i.ibb.co/TxsRmr2C/Screenshot-From-2025-03-16-17-33-06.png)

 - бот будет проверять новые сообщения через определённый интервал времени
