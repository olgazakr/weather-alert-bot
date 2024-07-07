import logging
import requests

from requests.exceptions import (HTTPError, Timeout,
                                 ConnectionError, RequestException)


async def make_request(lat: float, lon: float, token: str) -> list:
    """
    Asynchronously makes HTTP request to OpenWeatherMap API
    and returns response data. If request fails, returns error message.

    :param lat: latitude of location
    :param lon: longitude of location
    :param token: API token
    :return: dict with weather data or error message
    """
    logger = logging.getLogger('weather_request')
    with open('logs/weather_request_log.txt', 'a', encoding='utf-8') as file:
        file.write(f'{"-"*20}START REQUEST{"-"*20}\n')
        try:
            # Construct request URL
            url = (
                f'https://api.openweathermap.org/data/2.5/weather?'
                f'lat={lat}&lon={lon}&lang=ru&units=metric&appid={token}'
            )

            # Send request
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Parse response
            data = response.json()

            # Log incoming data
            logger.info(data)
            file.write(f'Incoming data: {data}\n')

            # Close log file and return data
            file.write(f'{"-"*20}END REQUEST{"-"*20}\n')
            return data
        except (ConnectionError, Timeout, HTTPError, RequestException) as error:
            # Log and return error message
            error_message = str(error)
            logger.error(error)
            file.write(f'{error_message}\n')
            file.write(f'{"-"*20}END REQUEST{"-"*20}\n')
            return {'error': error_message}
