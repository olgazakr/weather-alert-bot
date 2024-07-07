import logging
import requests

from requests.exceptions import (HTTPError, Timeout,
                                 ConnectionError, RequestException)


async def make_request(location: str, token: str) -> list:
    """
    Asynchronously makes HTTP request to OpenWeatherMap API
    and returns response data. If request fails, returns error message.

    :param location: location to search for
    :type location: str
    :param token: API token
    :type token: str
    :return: list of possible locations or error message
    :rtype: list or dict
    """
    logger = logging.getLogger('location_request')
    # Open log file and write start of request
    with open('logs/location_request_log.txt', 'a', encoding='utf-8') as file:
        file.write(f'{"-"*20}START REQUEST{"-"*20}\n')
        try:
            # Construct request URL
            url = (
                f'http://api.openweathermap.org/geo/1.0/direct?q={location}'
                f'&limit=5&appid={token}'
            )

            # Send request and check for errors
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Parse response JSON
            data = response.json()

            # Log incoming data and write to log file
            logger.info(data)
            file.write(f'Incoming data: {data}\n')

            # Create list of possible locations
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

            # Log list of possible locations and write to log file
            logger.info(possible_locations)
            file.write(f'Possible locations: {possible_locations}\n')
            file.write(f'{"-"*20}END REQUEST{"-"*20}\n')
            return possible_locations
        except (ConnectionError, Timeout, HTTPError, RequestException) as error:
            # Log error and write to log file
            error_message = str(error)
            logger.error(error_message)
            file.write(f'{error_message}\n')
            file.write(f'{"-"*20}END REQUEST{"-"*20}\n')
            # Return error message
            return {'error': error_message}
