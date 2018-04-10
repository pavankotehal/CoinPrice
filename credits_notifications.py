__author__ = 'Pavan Kotehal'

import requests
import time
from datetime import datetime
from config import key

CREDITS_PRICE_THRESHOLD = 1  # Set this to whatever you like
CREDITS_API_URL = 'https://api.coinmarketcap.com/v1/ticker/credits/'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/'+key
IFTTT_credits_price = 'https://maker.ifttt.com/trigger/credits_price_updates/with/key/'+key


def get_credits_price():
    response = requests.get(CREDITS_API_URL)
    response_json = response.json()
    # convert price into floating point number
    return float(response_json[0]['price_usd'])


def post_ifttt_webhook(event, value):
    # the payload that will be sent to IFTTT service
    data = {'value1': value}
    # inserts into desired event
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    # sends HTTP POST request  to a webhook url
    requests.post(ifttt_event_url, json=data)


def format_credits_history(credits_history):
    rows = []
    for credits_price in credits_history:
        # Formats the date into a string: '24.02.2018 15:09'
        date = credits_price['date'].strftime('%d.%m.%Y %H:%M')
        price = credits_price['price']
        # <b> (bold) tag creates bolded text
        # 24.02.2018 15:09: $<b>10123.4</b>
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    # Join the rows delimited by <br> tag: row1<br>row2<br>row3
    return '<br>'.join(rows)


def main():
    credits_history = []
    while True:
        price = get_credits_price()
        date = datetime.now()
        credits_history.append({'date': date, 'price': price})

        # send emergency notification
        if price > CREDITS_PRICE_THRESHOLD:
            post_ifttt_webhook('credits_price_emergency', price)

        # send telegram notification
        if len(credits_history) == 10:
            post_ifttt_webhook('credits_price_updates', format_credits_history(credits_history))

            # reset credits history

            credits_history = []
        # sleep for 5 mins
        # (for testing set it for lower number)
        time.sleep(10 * 60)
    pass


if __name__ == '__main__':
    main()
