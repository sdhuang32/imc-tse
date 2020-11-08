#!/usr/bin/env python3

import requests
import datetime
from urllib.parse import urljoin

def best_rate():
    url = "https://api.exchangeratesapi.io/"
    session = requests.Session()

    today = datetime.date.today()
    first_of_this_month = today.replace(day=1)
    last_of_last_month = first_of_this_month - datetime.timedelta(days=1)
    first_of_last_month = last_of_last_month.replace(day=1)

    aud_best_rate = 0
    best_rate_date = first_of_last_month
    tmp_date = first_of_last_month

    while tmp_date != first_of_this_month:
        target_date_str = tmp_date.strftime('%Y-%m-%d')
        url_with_date = urljoin(url, target_date_str)
        resp = requests.request('GET', url_with_date, timeout=10)

        aud_rate = resp.json().get('rates').get('AUD')
        if aud_rate >= aud_best_rate:
            aud_best_rate = aud_rate
            best_rate_date = tmp_date

        tmp_date = tmp_date + datetime.timedelta(days=1)

    session.close()
    return (best_rate_date.strftime('%Y-%m-%d'), aud_best_rate)
