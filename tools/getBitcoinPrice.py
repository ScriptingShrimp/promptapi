import requests

def get_btc_price():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    response = requests.get(url)
    data = response.json()
    price = data['bpi']['USD']['rate']
    return f"The current price of Bitcoin is ${price}"

btc = get_btc_price()
print(btc)