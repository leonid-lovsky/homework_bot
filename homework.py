import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv
from requests import RequestException

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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception as error:
        raise Exception(
            'Ошибка во время отправки сообщения в Telegram чат') from error
    else:
        logger.info(f'Бот отправил сообщение "{message}"')


def get_api_answer(current_timestamp):
    """Делает запрос к API-сервису."""
    try:
        timestamp = current_timestamp or int(time.time())
        params = {'from_date': timestamp}
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        if response != HTTPStatus.OK:
            raise RequestException(response)
    except Exception as error:
        raise Exception(
            'Ошибка во время выполнения запроса к API-сервису') from error
    else:
        logger.info(f'Выполнение запроса к API-сервису')
        return response.json()


def check_response(response):
    """Проверяет ответ API на корректность."""
    assert isinstance(response['homeworks'], list)
    return response['homeworks']


def parse_status(homework):
    """Извлекает статус домашней работы."""
    homework_name = homework['homework_name']
    homework_status = homework['status']
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяет доступность переменных окружения."""
    if PRACTICUM_TOKEN is None:
        logger.critical(
            'Отсутствует обязательная переменная окружения: '
            '"PRACTICUM_TOKEN"')
        return False
    if TELEGRAM_TOKEN is None:
        logger.critical(
            'Отсутствует обязательная переменная окружения: '
            '"TELEGRAM_TOKEN"')
        return False
    if TELEGRAM_CHAT_ID is None:
        logger.critical(
            'Отсутствует обязательная переменная окружения: '
            '"TELEGRAM_CHAT_ID"')
        return False
    return True


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        sys.exit("Не удалось установить переменные окружения.")

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())

    latest_error = None

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            for homework in homeworks:
                message = parse_status(homework)
                send_message(bot, message)
            current_timestamp = response['current_date']
        except Exception as error:
            logger.exception(error)
            if latest_error != error:
                if str(error):
                    message = f'Сбой в работе программы: {error}'
                else:
                    message = f'Сбой в работе программы.'
                send_message(bot, message)
                latest_error = error
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
