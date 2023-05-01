import platform

import aiohttp
import asyncio

from datetime import datetime, timedelta


async def main(d):

    all_rates=[]
    r={}
    rate={}

    async with aiohttp.ClientSession() as session:
        for date in d:
            try:
                async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}') as response:
                    if response.status == 200:
                        result = await response.json()
                        for val in result['exchangeRate']:
                            if val['currency'] == 'EUR':
                                r['EUR'] = {'sale': val['saleRateNB'], 'purchase': val['purchaseRateNB']}
                            if val['currency'] == 'USD':
                                r['USD'] = {'sale': val['saleRateNB'], 'purchase': val['purchaseRateNB']}
                        rate[date] = r
                        all_rates.append(rate)
                    else:
                        print(f"Error status: {resp.status}")
            except aiohttp.ClientConnectorError as err:
                print(f'Connection error', str(err))
        return (all_rates)


def get_date(days_to_subtract=10):

    dates = []

    if int(days_to_subtract)>10:
        days_to_subtract=10
    while int(days_to_subtract)>0:
        date = datetime.today() - timedelta(days=int(days_to_subtract))
        days_to_subtract=int(days_to_subtract)-1
        dates.append(date.strftime("%d.%m.%Y"))
    return dates


if __name__ == "__main__":
    days_to_subtract=input('введите колличество дней меньше 10ти >>> ')
    d = get_date(days_to_subtract)
    rates=asyncio.run(main(d))
    print(rates)