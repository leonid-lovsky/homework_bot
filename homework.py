import logging
import os
import sys
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
)


def send_message(bot, message):
    bot.send_message(TELEGRAM_CHAT_ID, message)


def get_api_answer(current_timestamp):
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    return requests.get(ENDPOINT, headers=HEADERS, params=params)


def check_response(response):
    return response.json()['homeworks']


def parse_status(homework):
    homework_name = homework['homework_name']
    homework_status = homework['status']
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    if PRACTICUM_TOKEN is not None:
        logging.critical(
            'Отсутствует обязательная переменная окружения: '
            '"PRACTICUM_TOKEN"')
        return False
    if TELEGRAM_TOKEN is not None:
        logging.critical(
            'Отсутствует обязательная переменная окружения: '
            '"TELEGRAM_TOKEN"')
        return False
    if TELEGRAM_CHAT_ID is not None:
        logging.critical(
            'Отсутствует обязательная переменная окружения: '
            '"TELEGRAM_CHAT_ID"')
        return False
    return True


def main():
    """Основная логика работы бота."""

    if not check_tokens():
        sys.exit(1)

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())

    ...

    while True:
        try:
            response = ...

            ...

            current_timestamp = ...
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            ...
            time.sleep(RETRY_TIME)
        else:
            ...


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        logging.critical(f'Программа принудительно остановлена.')
