# Homework-Bot
Telegram-бот, который обращается к API сервиса Практикум.Домашка и узнает статус домашней работы

## Зависимости
- flake8==3.9.2
- flake8-docstrings==1.6.0
- pytest==6.2.5
- python-dotenv==0.19.0
- python-telegram-bot==13.7
- requests==2.26.0

## Установка
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/leonid-lovsky/homework-bot.git
```

```
cd yatube
```

Создать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
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

Запустить проект:

```
python3 manage.py runserver
```
