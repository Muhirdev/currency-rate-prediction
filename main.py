import matplotlib.pyplot as plt
from datetime import timedelta
# O'zingiz yaratgan papka va fayldan funksiyani chaqiramiz
from exchange_rate_data.data_fetcher import get_cbu_data


def main():
    print("--- Valyuta kursi bashorati tizimi ---")

    # 1. Valyuta turini kiritish
    valyuta = input("Valyuta kodini kiriting (masalan: USD, EUR, RUB, GBP): ").upper()

    # 2. Bashorat davrini kiritish
    try:
        future_days = int(input(f"{valyuta} kursi necha kundan keyin qancha bo'lishini bilmoqchisiz?: "))
    except ValueError:
        print("Xato: Iltimos, kunni raqamda kiriting!")
        return

    # 3. Ma'lumotlarni olish (tahlil uchun 60 kunlik yetarli)
    df = get_cbu_data(currency_code=valyuta, days_count=60)

    if df is None or len(df) < 2:
        print(f"Xato: {valyuta} bo'yicha ma'lumot topilmadi yoki yetarli emas.")
        return

    # 4. Matematik Regressiya (y = w1*x + w0)
    start_date = df['Date'].min()
    df['Days'] = (df['Date'] - start_date).dt.days

    n = len(df)
    x = df['Days']
    y = df['Rate']

    # Chiziqli regressiya formulasi
    w1 = (n * (x * y).sum() - x.sum() * y.sum()) / (n * (x ** 2).sum() - (x.sum()) ** 2)
    w0 = (y.sum() - w1 * x.sum()) / n

    df['Trend'] = w1 * x + w0

    # 5. Kelajakni bashorat qilish
    today_num = df['Days'].max()
    target_day_num = today_num + future_days
    forecast_rate = w1 * target_day_num + w0
    forecast_date = df['Date'].max() + timedelta(days=future_days)

    # 6. Natijalarni chiqarish
    current_rate = df.iloc[-1]['Rate']
    print("\n" + "=" * 50)
    print(f"Tanlangan valyuta: {valyuta}")
    print(f"Bugungi kurs: {current_rate} UZS")
    print(f"Bashorat sanasi: {forecast_date.strftime('%d.%m.%Y')}")
    print(f"Kutilayotgan narx: {forecast_rate:.2f} UZS")
    print(f"Taxminiy o'zgarish: {forecast_rate - current_rate:+.2f} UZS")
    print("=" * 50)

    # 7. Grafik chizish
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Rate'], label=f'Haqiqiy {valyuta} kursi', color='gray', alpha=0.6)
    plt.plot(df['Date'], df['Trend'], label='Trend yo\'nalishi', color='blue', linestyle='--')

    # Bashorat nuqtasi
    plt.scatter(forecast_date, forecast_rate, color='red', s=100, label=f'Bashorat: {forecast_rate:.0f}', zorder=5)

    # Kelajakka yo'nalish chizig'i
    plt.plot([df['Date'].max(), forecast_date], [df.iloc[-1]['Trend'], forecast_rate], color='red', linestyle=':')

    plt.title(f"{valyuta}/UZS Kursi: O'tmish va {future_days} kunlik bashorat")
    plt.xlabel("Sana")
    plt.ylabel(f"Kurs ({valyuta} -> UZS)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()