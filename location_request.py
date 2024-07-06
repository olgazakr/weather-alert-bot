import logging
import requests

from requests.exceptions import HTTPError, Timeout, ConnectionError, RequestException


def make_request(location, token) -> list:
    logging.basicConfig(level=logging.INFO)
    
    try:
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={token}'

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        logging.info(data)

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

        return possible_locations
    except ConnectionError:
        logging.error(f'Connection error {ConnectionError.args}')
    except Timeout:
        logging.error(f'Timeout error {Timeout.args}')
    except HTTPError:
        logging.error(f'HTTP error {HTTPError.code}')
    except RequestException:
        logging.error(f'Request error {RequestException.code}')
    except Exception:
        logging.error(f'Unexpected error {Exception.args}')