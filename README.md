# FromExcelTGSender

## Описание
Бот, который рассылает сообщения по чатам по списку задач из Гугл таблицы (по расписанию)

## Запуск
```bash
cp .env.example .env
```

Впишите необходимые данные в переменные окружения:
```bash
SPREADSHEET_ID=
BOT_TOKEN=
MAIN_WORK_SHEET_ID=
```

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Структура
 - main.py - инициализация проекта, цикла проверки таблицы на новые сообщения
 - Model.py - модель сообщений (pydantic), валидаторы
 - GoogleSheets.py - работа с гугл таблицами, получение неотправленных сообщений, пометка отпралвенных
 - Bot.py - отправка сообщений

