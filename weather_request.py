import logging
import requests

from requests.exceptions import HTTPError, Timeout, ConnectionError, RequestException

async def make_request(lat, lon, token) -> list:
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

            user_response_data = str(data['weather'][0]['description']) + ', ' + \
                   str(data['main']['temp']) + '°C, скорость ветра: ' + \
                   str(data['wind']['speed']) + ' м/с'
            file.write(f'{"-"*20}END REQUEST{"-"*20}\n')
            return user_response_data
        except ConnectionError:
            error_message = "ConnectionError"
            logger.error(error_message)
            file.write(f'{error_message}\n')
            file.write(f'{"-"*20}END REQUEST{"-"*20}\n')
        except Timeout:
            error_message = "Timeout"
            logger.error(error_message)
            file.write(f'{error_message}\n')
            file.write(f'{"-"*20}END REQUEST{"-"*20}\n')
        except HTTPError:
            error_message = "HTTPError"
            logger.error(error_message)
            file.write(f'{error_message}\n')
            file.write(f'{"-"*20}END REQUEST{"-"*20}\n')
        except RequestException:
            error_message = "RequestException"
            logger.error(error_message)
            file.write(f'{error_message}\n')
            file.write(f'{"-"*20}END REQUEST{"-"*20}\n')