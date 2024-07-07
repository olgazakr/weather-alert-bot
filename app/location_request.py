import logging
import requests

from requests.exceptions import (HTTPError, Timeout,
                                 ConnectionError, RequestException)


async def make_request(location: str, token: str) -> list:
    logger = logging.getLogger('location_request')
    with open('logs/location_request_log.txt', 'a', encoding='utf-8') as file:
        file.write(f'{"-"*20}START REQUEST{"-"*20}\n')
        try:
            url = f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={token}'

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            logger.info(data)
            file.write(f'Incoming data: {data}\n')

            possible_locations = []
            for location in data:
                location_dict = {
                    'name': location['name'],
                    'country': location['country'],
                    'state': location['state'],
                    'lat': location['lat'],
                    'lon': location['lon']
                }
                possible_locations.append(location_dict)

            logger.info(possible_locations)
            file.write(f'Possible locations: {possible_locations}\n')
            file.write(f'{"-"*20}END REQUEST{"-"*20}\n')
            return possible_locations
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