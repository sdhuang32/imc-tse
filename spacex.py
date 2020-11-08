import json
import requests
import copy
import datetime
from urllib.parse import urljoin

class SpaceXData(object):

    def __init__(self, host='https://api.spacexdata.com', version='v3'):
        """
        Instantiate a new API client.
        Args:
        host (str): Hostname of the factomd instance.
        version (str): API version to use. This should remain 'v2'.
        """

        self.version = version
        self.host = host

        # Initialize the session.
        self.session = requests.Session()

    # Convenience method for building request URLs.
    @property
    def url(self):
        return urljoin(self.host, self.version)

    def handle_error_response(self, resp):
        print(resp)
        raise RuntimeError("Response code not 200 go check code")

    # Perform an API request.
    def _request(self, path, params=None):
        DEFAULT_TIMEOUT = 10
        fullpath = self.url + '/' + path
        resp = self.session.request('GET', fullpath, params=params, timeout=DEFAULT_TIMEOUT)

        # If something goes wrong, we'll pass the response
        # off to the error-handling code
        if resp.status_code >= 400:
            self.handle_error_response(resp)

        # Otherwise return the result dictionary.
        return resp.json()

    # API methods
    def get_launches(self, **kwargs):
        return self._request('launches/'.format(kwargs.get('path', '')), kwargs)

    def get_payloads(self, flight_number):
        """ Fetch Payloads """
        flight = self.get_launches(path='upcoming', flight_number=flight_number)[0]
        payloads = flight.get('rocket').get('second_stage').get('payloads')
        return payloads

    def get_launch_date_range(self, start_date, end_date):
        try:
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
            datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD!")

        flights = self.get_launches(start=start_date, end=end_date)
        if len(flights) == 0:
            return None

        return flights

    def get_heaviest_launch(self, start_date, end_date):
        flights = self.get_launch_date_range(start_date, end_date)
        if flights == None:
            return None

        heaviest_flight = flights[0]
        heaviest_payloads_kg = 0
        for flight in flights:
            payloads = flight.get('rocket').get('second_stage').get('payloads')

            total_weight = 0
            for payload in payloads:
                weight_kg = payload.get('payload_mass_kg')
                if weight_kg == None:
                    weight_kg = 0
                total_weight += weight_kg

            if total_weight > heaviest_payloads_kg:
                heaviest_payloads_kg = total_weight
                heaviest_flight = flight
                
        return heaviest_flight
