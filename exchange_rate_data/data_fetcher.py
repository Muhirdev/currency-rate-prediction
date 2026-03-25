import requests
import pandas as pd
from datetime import datetime, timedelta


def get_cbu_data(currency_code='USD', days_count=60):
    """
    Markaziy bankdan tanlangan valyuta (currency_code) bo'yicha
    oxirgi N kunlik ma'lumotni yig'ish.
    """
    data_list = []
    print(f"\n{currency_code} bo'yicha oxirgi {days_count} kunlik ma'lumotlar yig'ilmoqda...")

    for i in range(days_count):
        # Sanani orqaga qarab hisoblash
        target_date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        # URLga valyuta kodini joylashtiramiz
        url = f"https://cbu.uz/uz/arkhiv-kursov-valyut/json/{currency_code}/{target_date}/"

        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200 and response.json():
                item = response.json()[0]
                d = datetime.strptime(item['Date'], '%d.%m.%Y')
                rate = float(item['Rate'])
                data_list.append({'Date': d, 'Rate': rate})
        except:
            continue

    df = pd.DataFrame(data_list)
    if not df.empty:
        df = df.sort_values('Date').reset_index(drop=True)
    return df