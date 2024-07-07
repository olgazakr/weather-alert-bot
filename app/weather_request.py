import logging
import requests

from requests.exceptions import (HTTPError, Timeout,
                                 ConnectionError, RequestException)

async def make_request(lat: float, lon: float, token: str) -> list:
    logger = logging.getLogger('weather_request')
    with open('logs/weather_request_log.txt', 'a', encoding='utf-8') as file:
        file.write(f'{"-"*20}START REQUEST{"-"*20}\n')
        try:
            url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&lang=ru&units=metric&appid={token}'

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            logger.info(data)
            file.write(f'Incoming data: {data}\n')
            file.write(f'{"-"*20}END REQUEST{"-"*20}\n')
            return data
        except (ConnectionError, Timeout, HTTPError, RequestException) as error:
            error_message = str(error)
            logger.error(error)
            file.write(f'Error: {error}\n')
            file.write(f'{"-"*20}END REQUEST{"-"*20}\n')
            return {'error': error_message}