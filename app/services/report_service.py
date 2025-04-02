from app.db.models import Item, Brand, Model
from fastapi.responses import FileResponse
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import joinedload
from collections import defaultdict
from sqlalchemy.orm import Session
from app.db.session import get_db
from typing import Optional
from sqlalchemy import func
import pandas as pd
import requests


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


# - - - - - - - Tushumni olish uchun - - - - - - - -

def get_income_report(db: Session, period: Optional[str] = None,
                      start_date: Optional[str] = None, end_date: Optional[str] = None,
                      rate: Optional[float] = None, convert_to: str = "uzs"):
    today = datetime.now()

    # Sana oraliqlarini belgilash
    if period:
        if period == "daily":
            start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = today
        elif period == "weekly":
            start_date = today - timedelta(days=7)
            end_date = today
        elif period == "monthly":
            start_date = today - timedelta(days=30)
            end_date = today
        else:
            return {"error": "Invalid period. Choose from: daily, weekly, monthly"}
    elif start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}
    else:
        return {"error": "You must provide either 'period' or 'start_date' and 'end_date'"}

    # Sotuv ma'lumotlarini olish
    sales = db.query(Item).filter(
        Item.item_sold_date >= start_date,
        Item.item_sold_date <= end_date,
        Item.item_is_sold == True
    ).options(
        joinedload(Item.item_brand),
        joinedload(Item.item_model)
    ).all()

    # Valyuta kurslarini olish
    exchange_rates = get_exchange_rates()

    if convert_to == "usd" and rate is None:
        rate = exchange_rates.get("usd", 13000)

    # Valyuta bo‘yicha umumiy sotuvni hisoblash
    sales_by_currency = defaultdict(int)
    for sale in sales:
        sales_by_currency[sale.sold_currency] += sale.item_sold_price * sale.item_sold_quantity

    # Barcha summani `convert_to` valyutaga o'tkazish
    if convert_to not in exchange_rates:
        return {"error": "Invalid currency. Choose from: uzs, usd"}

    if convert_to == "usd" and rate:
        total_sales_converted = sum(
            amount * exchange_rates[currency] / rate
            for currency, amount in sales_by_currency.items()
        )
    else:
        total_sales_converted = sum(
            amount * exchange_rates[currency] / exchange_rates[convert_to]
            for currency, amount in sales_by_currency.items()
        )

    # Hisobot natijasi
    result = {
        "Oraliq": period if period else f"{start_date.date()} - {end_date.date()}",
        "Boshlang'ich sana": start_date.date().isoformat(),
        "Tugash sanasi": end_date.date().isoformat(),
        "Oraliqdagi umumiy tushum": round(total_sales_converted, 2),
        "Tanlangan valyuta": convert_to.upper(),
        "Mahsulot ma'lumotlari": [
            {
                "Brand": sale.item_brand.brand_name if sale.item_brand else "Noma'lum",
                "Model": sale.item_model.model_name if sale.item_model else "Noma'lum",
                "Sotilgan miqdori": sale.item_sold_quantity,
                "Sotilgan summasi": sale.item_sold_price,
                "Sotilgan valyutasi": sale.sold_currency,
                "Tovardan qolgan foyda": sale.item_sold_price - sale.item_purchased_price,
                "Sotilgan Sanasi": sale.item_sold_date.strftime("Sana: %Y-%m-%d, Vaqt: %H-%M-%S"),
                "Umumiy sotilgan summasi": sale.item_sold_price * sale.item_sold_quantity
            }
            for sale in sales
        ]
    }
    print(f"Oraliqdagi umumiy tushum: {result["Oraliqdagi umumiy tushum"]}")
    return result


def save_income_report_to_excel(db: Session, period: Optional[str] = None,
                                start_date: Optional[str] = None, end_date: Optional[str] = None,
                                rate: Optional[float] = None, convert_to: str = "uzs"):
    report = get_income_report(db, period, start_date, end_date, rate, convert_to)

    if "error" in report:
        return report  # Xatolik bo'lsa, xatolikni qaytaramiz

    data = report["Mahsulot ma'lumotlari"]

    df = pd.DataFrame(data)  # Pandas DataFrame ga o'tkazamiz

    file_path = "income_report.xlsx"
    df.to_excel(file_path, index=False)  # Excel fayl sifatida saqlaymiz

    return FileResponse(file_path,
                        filename="income_report.xlsx",
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# - - - - - - - Chiqimni olish uchun - - - - - - - -

def get_expense_report(db: Session, period: Optional[str] = None,
                       start_date: Optional[str] = None,
                       end_date: Optional[str] = None,
                       rate: Optional[float] = None,
                       convert_to: str = "uzs"):
    today = datetime.now()

    # Sana oraliqlarini belgilash
    if period:
        if period == "daily":
            start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = today
        elif period == "weekly":
            start_date = today - timedelta(days=7)
            end_date = today
        elif period == "monthly":
            start_date = today - timedelta(days=30)
            end_date = today
        else:
            return {"error": "Invalid period. Choose from: daily, weekly, monthly"}
    elif start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}
    else:
        return {"error": "You must provide either 'period' or 'start_date' and 'end_date'"}

    # Ma'lumotlarni olish
    # expenses = db.query(Item).filter(Item.item_purchased_date.between(start_date, end_date)).all()
    expenses = db.query(Item).filter(
        Item.item_purchased_date >= start_date,
        Item.item_purchased_date <= end_date,
        # Item.item_is_sold == False
    ).options(
        joinedload(Item.item_brand),
        joinedload(Item.item_model)
    ).all()

    exchange_rates = get_exchange_rates()

    expenses_by_currency = defaultdict(int)

    for expense in expenses:
        total_sum = expense.item_purchased_price * expense.item_purchased_quantity
        print(f"Brand: {expense.item_brand.brand_name}, Total Sum: {total_sum}")

        expenses_by_currency[
            expense.purchased_currency] += expense.item_purchased_price * expense.item_purchased_quantity

    # Barcha summani `convert_to` valyutaga o'tkazish
    if convert_to not in exchange_rates:
        return {"error": "Invalid currency. Choose from: uzs, usd"}

    if convert_to == "usd" and rate is None:
        total_expenses_converted = sum(
            amount * exchange_rates[currency] / exchange_rates[convert_to]
            for currency, amount in expenses_by_currency.items()
        )
    elif convert_to == "usd" and rate:
        total_expenses_converted = sum(
            amount * exchange_rates[currency] / rate
            for currency, amount in expenses_by_currency.items()
        )
    else:
        total_expenses_converted = sum(
            amount * exchange_rates[currency] / exchange_rates[convert_to]
            for currency, amount in expenses_by_currency.items()
        )

    total_expense_sum = sum(
        expense.item_purchased_price * expense.item_purchased_quantity for expense in expenses
    )

    result = {
        "Oraliq": period if period else f"{start_date.date()} - {end_date.date()}",
        "Boshlang'ich sana": start_date.date().isoformat(),
        "Tugash sanasi": end_date.date().isoformat(),
        "Oraliqdagi umumiy xarajat": round(total_expenses_converted, 2),
        "Markaziy bankning dollar kursi": exchange_rates[convert_to],
        "Tanlangan valyuta": convert_to.upper(),
        "Umumiy sotib olingan summasi": round(total_expense_sum, 2),  # Umumiy summa kiritildi
        "Mahsulot ma'lumotlari": [
            {
                "Brand": expense.item_brand.brand_name,
                "Model": expense.item_model.model_name,
                "Sotib olingan miqdori": expense.item_purchased_quantity,
                "Sotib olingan summasi": round(expense.item_purchased_price, 2),
                "Sotib olingan valyutasi": expense.purchased_currency,
                "Sotib olingan sana": expense.item_purchased_date.strftime("%Y-%m-%d"),
                "Sotib olingan vaqt": expense.item_purchased_date.strftime("%H:%M:%S"),
                "Umumiy sotib olingan summasi": round(
                    expense.item_purchased_price * expense.item_purchased_quantity, 2
                )
            }
            for expense in expenses
        ]
    }

    print(f"Umumiy summa: {result['Umumiy sotib olingan summasi']}")  # Endi ishlaydi
    return result


# - - - - - - - - - Omborxonadagi sotilmagan mahsulotlar - - - - - - - - -

def get_stock_with_value(db: Session):
    result = db.query(
        Item.item_brand_id,
        Brand.brand_name,
        Item.item_model_id,
        Model.model_name,
        Item.item_color,
        Item.item_ram,
        Item.item_barcode,
        (func.coalesce(func.sum(Item.item_purchased_quantity), 0) -
         func.coalesce(func.sum(Item.item_sold_quantity), 0)).label("remaining_quantity"),
        Item.purchased_currency,
        func.coalesce(func.sum((Item.item_purchased_price * Item.item_purchased_quantity) -
                               (Item.item_sold_price * Item.item_sold_quantity)), 0).label("remaining_value")
    ).join(Brand, Item.item_brand_id == Brand.id) \
        .join(Model, Item.item_model_id == Model.id) \
        .group_by(
        Item.item_brand_id,
        Brand.brand_name,
        Item.item_model_id,
        Model.model_name,
        Item.item_color,
        Item.item_ram,
        Item.item_barcode,
        Item.purchased_currency
    ).having(
        func.sum(Item.item_purchased_quantity) - func.sum(func.coalesce(Item.item_sold_quantity, 0)) > 0
    ).all()

    return [
        {
            "brand": row.brand_name,
            "brand_id": row.item_brand_id,
            "model": row.model_name,
            "model_id": row.item_model_id,
            "color": row.item_color,
            "ram": row.item_ram if row.item_ram else "N/A",
            "barcode": row.item_barcode,
            "remaining_quantity": row.remaining_quantity,
            "remaining_value": round(row.remaining_value, 2) if row.remaining_value else 0,
            "currency": row.purchased_currency
        }
        for row in result
    ]


# - - - - - - Oraliqdagi umumiy tushum va eng ko'p sotilgan mahsulotlarni olish - - - - - -

def get_statistics(db: Session,
                   period: Optional[str] = None,
                   start_date: Optional[str] = None,
                   end_date: Optional[str] = None,
                   rate: Optional[float] = None,
                   convert_to: str = "uzs",
                   lang: str = "uz"):
    today = datetime.now()

    if period:
        if period == "daily":
            start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = today
        elif period == "weekly":
            start_date = today - timedelta(days=7)
            end_date = today
        elif period == "monthly":
            start_date = today - timedelta(days=30)
            end_date = today
        else:
            return {"error": "Invalid period. Choose from: daily, weekly, monthly"}
    elif start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}
    else:
        return {"error": "You must provide either 'period' or 'start_date' and 'end_date'"}

    sales = db.query(Item).filter(
        Item.item_sold_date >= start_date,
        Item.item_sold_date <= end_date,
        Item.item_is_sold == True
    ).options(
        joinedload(Item.item_brand),
        joinedload(Item.item_model),
        joinedload(Item.item_category)
    ).all()

    exchange_rates = get_exchange_rates()

    sales_by_currency = defaultdict(int)
    sales_by_product = defaultdict(int)

    for sale in sales:
        # Sotilgan valyutani hisoblash
        sales_by_currency[sale.sold_currency] += sale.item_sold_price * sale.item_sold_quantity

        # Mahsulot bo'yicha sotuvlar
        product_key = (sale.item_brand.brand_name, sale.item_model.model_name)
        sales_by_product[product_key] += sale.item_sold_quantity * sale.item_sold_price


    # Barcha summani convert to valyutaga o'tkazish
    if convert_to not in exchange_rates:
        return {"error": "Invalid currency. Choose from: uzs, usd"}

    if convert_to == "usd" and rate is None:
        total_sales_converted = sum(
            amount * exchange_rates[currency] / exchange_rates[convert_to]
            for currency, amount in sales_by_currency.items()
        )
    elif convert_to == "usd" and rate:
        total_sales_converted = sum(
            amount * exchange_rates[currency] / rate
            for currency, amount in sales_by_currency.items()
        )
    else:
        total_sales_converted = sum(
            amount * exchange_rates[currency] / exchange_rates[convert_to]
            for currency, amount in sales_by_currency.items()
        )

    # Eng ko'p sotilgan mahsulotni topish
    best_selling_product = max(sales_by_product, key=sales_by_product.get)

    # Eng ko'p sotilgan mahsulot bo'yicha umumiy summani hisoblash
    best_selling_total = sales_by_product[best_selling_product]

    result = {
        "Oraliq": period if period else f"{start_date.date()} - {end_date.date()}",
        "Boshlang'ich sana": start_date.isoformat(),
        "Tugash sanasi": end_date.isoformat(),
        "Umumiy daromad": round(total_sales_converted, 2),
        "Tanlangan valyuta": convert_to.upper(),
        "Eng ko'p sotilgan mahsulot": {
            "Brend": best_selling_product[0],
            "Model": best_selling_product[1],
            "Sotilgan miqdori": sales_by_product[best_selling_product] / best_selling_total if best_selling_total > 0 else 0,
            "Umumiy summasi": best_selling_total
        }
    }
    print(f"Tanlangan til: {lang}")
    return result
