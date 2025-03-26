# from datetime import timedelta, datetime
# from app.db.schemas import ReportSchema
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.db.models import Transaction
# from app.db.session import get_db
# from app.db.models import Item
#
#
# # router = APIRouter()
# #
# # @router.get("/income-expense", response_model=list[ReportSchema])
# def get_report(period: str, db: Session = Depends(get_db)):
#     now = datetime.now()
#
#     if period == "daily":
#         start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
#     elif period == "weekly":
#         start_date = now - timedelta(days=now.weekday())
#         start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
#     elif period == "monthly":
#         start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#     else:
#         return {"error": "Xato oraliq. Tanlang: daily, weekly, monthly"}
#
#     # Ma'lumot olish
#     # Belgilangan sanadan boshlab yuqorisini ko'rsatadi
#
#     sales = db.query(Item).filter(Item.item_sold_date >= start_date).all()
#
#     # Hisobot yaratish
#
#     total_sales = sum(sale.item_sold_price for sale in sales)
#     result = {
#         "period": period,
#         "total_sales": total_sales,
#         currency
#     }
#
#
#
#
#
#
#
#
#
#
#
#
# #     transactions = (
# #         db.query(Transaction)
# #         .filter(Transaction.date >= start_date)
# #         .order_by(Transaction.date)
# #         .all()
# #     )
# #
# #     report = {}
# #
# #     for trx in transactions:
# #         date_key = trx.date.strftime("%Y-%m-%d")
# #         if date_key not in report:
# #             report[date_key] = {"period": date_key, "total_income": 0, "total_expense": 0}
# #
# #         report[date_key]["total_income"] += trx.income
# #         report[date_key]["total_expense"] += trx.expense
# #
# #     return list(report.values())

import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from collections import defaultdict
from app.db.models import Item
from app.db.session import get_db

router = APIRouter()


# Valyuta kurslarini API orqali olish
def get_exchange_rates():
    try:
        response = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json")
        data = response.json()
        rates = {"uzs": 1}
        for item in data:
            rates[item["Ccy"].lower()] = float(item["Rate"])
        return rates
    except Exception as e:
        print(f"Valyutalar kursini olishda xatolik: {e}")
        return {"usd": 13000, "uzs": 1}

# Hisobot API
@router.get("/report")
def get_report(period: str, convert_to: str = "uzs", db: Session = Depends(get_db)):
    today = datetime.now()

    if period == "daily":
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "weekly":
        start_date = today - timedelta(days=7)
    elif period == "monthly":
        start_date = today - timedelta(days=30)
    else:
        return {"error": "Invalid period. Choose from: daily, weekly, monthly"}

    # Ma'lumotlarni olish
    sales = db.query(Item).filter(Item.item_sold_date >= start_date).all()

    # Valyuta kurslarini olish
    exchange_rates = get_exchange_rates()
    # print(f"Exchange_rates: {exchange_rates}")

    # Valyuta bo‘yicha umumiy sotuvni hisoblash
    sales_by_currency = defaultdict(int)
    for sale in sales:

        print(f"Sale price: {sale.item_sold_price, 2}")
        print(f"Sale quantity: {sale.item_sold_quantity}")
        print(f"Total summa: {sale.item_sold_quantity * sale.item_sold_price}\n")

        sales_by_currency[sale.sold_currency] +=sale.item_sold_price * sale.item_sold_quantity
        print(f"sales_by_currency: {sales_by_currency.items()}")
#                                                                        usd                           120                 1
#         print(f"salas by currency: {sales_by_currency}, sales_by_currency[sale.sold_currency]: {sales_by_currency[sale.sold_currency]}"
#               f"sale.item_sold_price: {sale.item_sold_price}, sale.item_sold_quantity: {sale.item_sold_quantity}")
    # Barcha summani `convert_to` valyutaga o‘tkazish
    if convert_to not in exchange_rates:
        return {"error": "Invalid currency. Choose from: uzs, usd"}

    total_sales_converted = sum(
        amount * exchange_rates[currency] / exchange_rates[convert_to]
        for currency, amount in sales_by_currency.items()
    )

    # for currency, amount in sales_by_currency.items():
    #     total_sales_converted = sum(amount * exchange_rates[currency] / exchange_rates[convert_to])

    # Hisobot natijasi
    result = {
        "Oraliq": period,
        "Oraliqdagi umumiy tushum": round(total_sales_converted, 2),
        "Tanlangan valyuta": convert_to.upper(),
        "Mahsulot ma'lumotlari": [
            {
                "Brand": sale.item_brand.brand_name,
                "Model": sale.item_model.model_name,
                "Sotilgan miqdori": sale.item_sold_quantity,
                "Sotilgan summasi": sale.item_sold_price,
                "Sotilgan valyutasi": sale.sold_currency,
                "Sotilgan Sanasi": sale.item_sold_date.strftime("%Y-%m-%d"),
                "Umumiy sotilgan summasi": sale.item_sold_price * sale.item_sold_quantity
                
            }
            for sale in sales
        ]
    }
    return result
