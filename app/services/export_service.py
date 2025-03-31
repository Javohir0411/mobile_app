from app.services.report_service import get_income_report, get_expense_report
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from app.db.dynamic_search import detect_language
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from reportlab.lib import colors
from app.db.models import Item
from typing import Optional
import pandas as pd
import os


# --------- tushumni excelga saqlash --------------------

def income_to_excel(db: Session, period: Optional[str] = None, start_date: Optional[str] = None,
                    end_date: Optional[str] = None, rate: Optional[float] = None, convert_to: str = "uzs"):
    report = get_income_report(db, period, start_date, end_date, rate, convert_to)
    total_income = report.get("Oraliqdagi umumiy tushum", 2)
    print(f"Oraliqdagi umumiy tushum: {total_income} {report.get('Tanlangan valyuta')}")

    if "error" in report:
        return report  # Xatolik bo'lsa, xatolikni qaytaramiz

    data = report["Mahsulot ma'lumotlari"]
    # print(f"data: {data}")
    if not data:
        return {"error": {"Berilgan oraliqda ma'lumot yo'q"}}

    # Valyutani faqat nomini olish uchun `.name` ishlatamiz
    for item in data:
        item["Sotilgan valyutasi"] = item["Sotilgan valyutasi"].name  # USD, UZS ko‘rinishida chiqarish uchun

    df = pd.DataFrame(data)  # Pandas DataFrame ga o'tkazamiz
    print(f"df column: {df.columns}")

    # Ustunlar tartibini belgilash
    df = df[["Brand", "Model", "Sotilgan miqdori", "Sotilgan summasi", "Sotilgan valyutasi", "Tovardan qolgan foyda",
             "Sotilgan Sanasi", "Umumiy sotilgan summasi"]]

    # Bo'sh qator
    empty_row = pd.DataFrame({col: [""] for col in df.columns})

    # Umumiy tushumni alohida qo‘shish
    total_income_row = pd.DataFrame({
        "Brand": ["Jami"],
        "Model": [""],
        "Sotilgan miqdori": [""],
        "Sotilgan summasi": [""],
        "Sotilgan valyutasi": [report.get("Tanlangan valyuta")],
        "Tovardan qolgan foyda": [""],
        "Sotilgan Sanasi": [""],
        "Umumiy sotilgan summasi": [total_income]
    })

    # DataFrame-ga qo‘shamiz
    df = pd.concat([df, empty_row, total_income_row], ignore_index=True)

    file_path = "income_report.xlsx"
    df.to_excel(file_path, index=False)  # Excel fayl sifatida saqlaymiz

    return FileResponse(file_path,
                        filename="income_report.xlsx",
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# --------- chiqimni excelga saqlash --------------------

def expense_to_excel(db: Session, period: Optional[str] = None,
                     start_date: Optional[str] = None, end_date: Optional[str] = None,
                     rate: Optional[float] = None, convert_to: str = "uzs"):
    report = get_expense_report(db, period, start_date, end_date, rate, convert_to)
    total_income = report.get("Oraliqdagi umumiy tushum", 2)
    print(f"Oraliqdagi umumiy tushum: {total_income} {report.get('Tanlangan valyuta')}")

    if "error" in report:
        return report  # Xatolik bo'lsa, xatolikni qaytaramiz

    data = report["Mahsulot ma'lumotlari"]
    # print(f"data: {data}")
    if not data:
        return {"error": {"Berilgan oraliqda ma'lumot yo'q"}}

    # Valyutani faqat nomini olish uchun `.name` ishlatamiz
    for item in data:
        item["Sotib olingan valyutasi"] = item["Sotib olingan valyutasi"].name  # USD, UZS ko‘rinishida chiqarish uchun

    df = pd.DataFrame(data)  # Pandas DataFrame ga o'tkazamiz
    print(f"df column: {df.columns}")

    # Ustunlar tartibini belgilash
    df = df[["Brand", "Model", "Sotib olingan miqdori", "Sotib olingan summasi", "Sotib olingan valyutasi",
             "Sotib olingan sana", "Sotib olingan vaqt", "Umumiy sotib olingan summasi"]]

    expenses = db.query(Item).filter(Item.item_purchased_date.between(start_date, end_date)).all()
    last_expense = expenses[-1] if expenses else None

    # Bo'sh qator
    empty_row = pd.DataFrame({col: [""] for col in df.columns})

    # Umumiy tushumni alohida qo‘shish
    total_income = report.get("Oraliqdagi umumiy xarajat", 2)
    total_income_row = pd.DataFrame({
        "Brand": ["Jami"],
        "Model": [""],
        "Sotib olingan miqdori": [""],
        "Sotib olingan summasi": [""],
        "Sotib olingan valyutasi": [report.get("Tanlangan valyuta")],
        "Sotib olingan sana": last_expense.item_purchased_date.strftime("%Y-%m-%d") if last_expense else "",
        "Sotib olingan vaqt": last_expense.item_purchased_date.strftime("%H:%M:%S") if last_expense else "",
        "Umumiy sotib olingan summasi": [total_income]
    })

    df = pd.concat([df, empty_row, total_income_row], ignore_index=True)

    file_path = "expense_report.xlsx"
    df.to_excel(file_path, index=False)  # Excel fayl sifatida saqlaymiz

    return FileResponse(file_path,
                        filename="expense_report.xlsx",
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# -----------------------------------------------------


def items_to_excel(db):
    try:
        items = db.query(Item).all()  # Barcha mahsulotlarni olish

        # Ma'lumotlarni DataFrame ga o'tkazamiz
        data = [{
            "ID": item.id,
            "Kategoriya": (
                item.item_category.category_name_uz
                if item.item_category and detect_language(item.item_category.category_name_uz) == "uz"
                else item.item_category.category_name_ru if item.item_category
                else "Noma'lum"
            ),
            "Brend": item.item_brand.brand_name if item.item_brand else "Noma'lum",
            "Model": item.item_model.model_name if item.item_model else "Noma'lum",
            "Sotib olingan narxi": item.item_purchased_price,
            "Sotib olingan valyuta": item.purchased_currency.name if item.purchased_currency else "Noma'lum",
            "Sotilgan narxi": item.item_sold_price,
            "Sotilgan valyuta": item.sold_currency.name if item.sold_currency else "Noma'lum"
        } for item in items]

        df = pd.DataFrame(data)

        file_path = "hisobot.xlsx"
        df.to_excel(file_path, index=False)

        return FileResponse(file_path,
                            filename="hisobot.xlsx",
                            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        return {"error": f"Excelga saqlashda xatolik: {str(e)}"}


# - - - - - - - - PDF faylga eksport qilish - - - - - - - -

def generate_pdf_income_report(report_data, pdf_filename):
    pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)
    elements = []

    headers = ["Brand", "Model", "Sotilgan miqdori", "Sotilgan summasi", "Sotilgan valyutasi",
               "Foyda", "Sotilgan sana", "Sotilgan vaqt", "Umumiy sotilgan summa"]

    data = [headers] + [
        [
            item["Brand"],
            item["Model"],
            item["Sotilgan miqdori"],
            f"{item['Sotilgan summasi']:,.2f}",
            str(item["Sotilgan valyutasi"]).split(".")[-1],  # Valyutani oddiy satrga o‘giramiz
            f"{item['Tovardan qolgan foyda']:,.2f}",
            item["Sotilgan Sanasi"].replace("Sana: ", "").split(",")[0],
            # "Sana:" olib tashlanadi va faqat sana olinadi
            item["Sotilgan Sanasi"].split(", ")[1] if ", " in item["Sotilgan Sanasi"] else "-",
            # Vaqtni olish yoki "-" qo‘yish
            f"{item['Umumiy sotilgan summasi']:,.2f}"
        ]
        for item in report_data["Mahsulot ma'lumotlari"]
    ]

    col_widths = [60, 60, 40, 70, 50, 70, 70, 50, 80]  # Har bir ustun uchun kenglik

    jami_tushum = report_data["Oraliqdagi umumiy tushum"]
    data.append([""] * 7 + ["Jami tushum", f"{jami_tushum}"])
    print(f"data.get('Oraliqdagi umumiy tushum'): {jami_tushum}")
    print(f"data: {data}")

    table = Table(data, colWidths=col_widths)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),  # Matnni kichikroq qilish
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('WORDWRAP', (0, 0), (-1, -1))  # Matnni sig‘dirish
    ])

    table.setStyle(style)
    elements.append(table)

    pdf.build(elements)


# def download_income_report(period: Optional[str] = None, period_date: Optional[str] = None,
#                            rate: Optional[float] = None, convert_to: str = "uzs", ):
#     result = get_income_report(db, period, period_date, rate, convert_to)
#     if "error" in result:
#         return {"error": result["error"]}
#
#     pdf_filename = "income_report.pdf"
#     generate_pdf_report(result, pdf_filename)
#
#     return FileResponse(pdf_filename, media_type="application/pdf", filename=pdf_filename)
#
#
# # - - - - - - - - - Chiqim uchun pdf fayl - - - - - - - -
#
# def generate_expense_pdf_report(report_data, pdf_filename):
#     pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)
#     elements = []
#
#     headers = ["Brand", "Model", "Sotib olingan miqdori", "Sotib olingan summasi",
#                "Sotib olingan valyutasi", "Sotib olingan sana",
#                "Sotib olingan vaqt", "Umumiy sotib olingan summa"]
#
#     data = [headers]
#
#     umumiy_xarajat = report_data.get("Oraliqdagi umumiy xarajat")
#     print(f"umumiy_xarajat: {umumiy_xarajat}")
#     for item in report_data.get("Mahsulot ma'lumotlari", []):
#         umumiy_sotib_olingan_summasi = item.get("Umumiy sotib olingan summasi", 0)
#         data.append([
#             item.get("Brand", "-"),
#             item.get("Model", "-"),
#             item.get("Sotib olingan miqdori", 0),
#             f"{item.get('Sotib olingan summasi', 0):,.2f}",
#             str(item["Sotib olingan valyutasi"]).split(".")[-1],
#             item.get("Sotib olingan sana", "-"),
#             item.get("Sotib olingan vaqt", "-"),
#             f"{umumiy_sotib_olingan_summasi:,.2f}"
#         ])
#
#
#     table = Table(data, colWidths=[70, 70, 60, 80, 50, 70, 50, 90])
#
#     table.setStyle(TableStyle([
#         ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
#         ('FONTSIZE', (0, 0), (-1, -1), 8),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
#         ('PADDING', (0, 0), (-1, -1), 2),
#     ]))
#
#     elements.append(table)
#     pdf.build(elements)

def generate_expense_pdf_report(report_data, pdf_filename):
    pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)
    elements = []

    headers = ["Brand", "Model", "Miqdori", "Summasi", "Valyutasi", "Sana", "Vaqt", "Umumiy summa", "Jami xarajat"]

    data = [headers] + [
        [
            item["Brand"],
            item["Model"],
            item["Sotib olingan miqdori"],
            f"{item['Sotib olingan summasi']:,.2f}",
            str(item["Sotib olingan valyutasi"]).split(".")[-1],  # Valyutani oddiy satrga o‘giramiz
            item["Sotib olingan sana"],
            item["Sotib olingan vaqt"],
            f"{item['Umumiy sotib olingan summasi']:,.2f}",
            report_data["Tanlangan valyuta"]
        ]
        for item in report_data["Mahsulot ma'lumotlari"]
    ]

    col_widths = [70, 70, 40, 70, 50, 70, 70, 70, 70]  # Har bir ustun uchun kenglik

    jami_xarajat = report_data["Oraliqdagi umumiy xarajat"]
    data.append([""] * 7 + [jami_xarajat, report_data["Tanlangan valyuta"]])
    # print(f"data.get('Oraliqdaga

    table = Table(data, colWidths=col_widths)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),  # Matnni kichikroq qilish
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('WORDWRAP', (0, 0), (-1, -1))  # Matnni sig‘dirish
    ])

    table.setStyle(style)
    elements.append(table)

    pdf.build(elements)


# def generate_expense_pdf_report(db: Session,
#                                 period: Optional[str] = None,
#                                 start_date: Optional[str] = None,
#                                 end_date: Optional[str] = None,
#                                 rate: Optional[float] = None,
#                                 convert_to: str = "uzs"):
#     if start_date and end_date:
#         try:
#             start_date = datetime.strptime(start_date, "%Y-%m-%d")
#             end_date = datetime.strptime(end_date, "%Y-%m-%d")
#         except ValueError:
#             return {"error": "Invalid date format. Use YYYY-MM-DD"}
#     elif period:
#         today = datetime.now()
#         if period == "daily":
#             start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
#             end_date = today.replace(hour=23, minute=59, second=59)
#         elif period == "weekly":
#             start_date = today - timedelta(days=7)
#             end_date = today
#         elif period == "monthly":
#             start_date = today - timedelta(days=30)
#             end_date = today
#         else:
#             return {"error": "Invalid period. Choose from: daily, weekly, monthly"}
#     else:
#         return {"error": "Either period or start_date and end_date must be provided"}
#
#     # Ma'lumotlarni olish
#     expenses = db.query(Item).filter(Item.item_purchased_date.between(start_date, end_date)).all()
#
#     exchange_rates = get_exchange_rates()
#     if convert_to not in exchange_rates:
#         return {"error": "Invalid currency. Choose from: uzs, usd"}
#
#     total_expenses_converted = 0
#     converted_expenses = []
#
#     for expense in expenses:
#         total_sum = expense.item_purchased_price * expense.item_purchased_quantity
#         currency = expense.purchased_currency  # Sotib olingan valyuta
#
#         # Konvertatsiya qilish
#         if convert_to == "usd":
#             if rate is None:
#                 if currency in exchange_rates:
#                     converted_total = total_sum * (exchange_rates[convert_to] / exchange_rates[currency])
#                 else:
#                     raise ValueError(f"Valyuta kursi topilmadi: {currency}")
#             else:
#                 converted_total = total_sum / rate
#         else:  # UZS yoki boshqa valyuta
#             if currency in exchange_rates and convert_to in exchange_rates:
#                 converted_total = total_sum * (exchange_rates[convert_to] / exchange_rates[currency])
#             else:
#                 raise ValueError(f"Valyuta kursi topilmadi: {currency} yoki {convert_to}")
#
#         total_expenses_converted += converted_total
#
#         # Hisobot uchun ma'lumotlar
#         converted_expenses.append({
#             "Brand": expense.item_brand.brand_name,
#             "Model": expense.item_model.model_name,
#             "Sotib olingan miqdori": expense.item_purchased_quantity,
#             "Sotib olingan summasi": round(expense.item_purchased_price, 2),
#             "Sotib olingan valyutasi": convert_to.upper(),  # Konvertatsiya qilingan valyutani ishlatish
#             "Sotib olingan sana": expense.item_purchased_date.strftime("%Y-%m-%d"),
#             "Sotib olingan vaqt": expense.item_purchased_date.strftime("%H:%M:%S"),
#             "Umumiy sotib olingan summa": round(converted_total, 2)  # Konvertatsiya qilingan summa
#         })
# #
#     # Hisobot natijasi
#     result = {
#         "Oraliq": period if period else f"{start_date.date()} - {end_date.date()}",
#         "Boshlang'ich sana": start_date.date().isoformat(),
#         "Tugash sanasi": end_date.date().isoformat(),
#         "Markaziy bankning dollar kursi": exchange_rates["usd"],
#         "Tanlangan valyuta": convert_to.upper(),
#         "Mahsulot ma'lumotlari": converted_expenses
#     }
#
#     return result

# def generate_expense_pdf_report(db: Session, period: Optional[str] = None,
#                                 start_date: Optional[str] = None,
#                                 end_date: Optional[str] = None,
#                                 rate: Optional[float] = None,
#                                 convert_to: str = "uzs"):
#     if start_date and end_date:
#         try:
#             start_date = datetime.strptime(start_date, "%Y-%m-%d")
#             end_date = datetime.strptime(end_date, "%Y-%m-%d")
#         except ValueError:
#             return {"error": "Invalid date format. Use YYYY-MM-DD"}
#     elif period:
#         today = datetime.now()
#         if period == "daily":
#             start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
#             end_date = today.replace(hour=23, minute=59, second=59)
#         elif period == "weekly":
#             start_date = today - timedelta(days=7)
#             end_date = today
#         elif period == "monthly":
#             start_date = today - timedelta(days=30)
#             end_date = today
#         else:
#             return {"error": "Invalid period. Choose from: daily, weekly, monthly"}
#     else:
#         return {"error": "Either period or start_date and end_date must be provided"}
#
#     # Ma'lumotlarni olish
#     expenses = db.query(Item).filter(Item.item_purchased_date.between(start_date, end_date)).all()
#
#     exchange_rates = get_exchange_rates()
#     if convert_to not in exchange_rates:
#         return {"error": "Invalid currency. Choose from: uzs, usd"}
#
#     converted_expenses = []
#
#     for expense in expenses:
#         total_sum = expense.item_purchased_price * expense.item_purchased_quantity
#
#         # Konvertatsiya qilish
#         if convert_to == "usd" and rate is None:
#             converted_total = total_sum / exchange_rates[expense.purchased_currency] * exchange_rates["usd"]
#         elif convert_to == "usd" and rate:
#             converted_total = total_sum / rate
#         else:
#             converted_total = total_sum  # UZS bo‘lsa, o‘zgartirilmaydi
#
#         # 🔹 **Hisobot uchun ma'lumotlar**
#         converted_expenses.append({
#             "Brand": expense.item_brand.brand_name,
#             "Model": expense.item_model.model_name,
#             "Sotib olingan miqdori": expense.item_purchased_quantity,
#             "Sotib olingan summasi": round(expense.item_purchased_price, 2),
#             "Sotib olingan valyutasi": convert_to.upper(),  # Konvertatsiya qilingan valyutani ishlatish
#             "Sotib olingan sana": expense.item_purchased_date.strftime("%Y-%m-%d"),
#             "Sotib olingan vaqt": expense.item_purchased_date.strftime("%H:%M:%S"),
#             "Umumiy sotib olingan summa": round(converted_total, 2)  # Konvertatsiya qilingan summa
#         })
#
#     # Hisobot natijasi
#     result = {
#         "Oraliq": period if period else f"{start_date.date()} - {end_date.date()}",
#         "Boshlang'ich sana": start_date.date().isoformat(),
#         "Tugash sanasi": end_date.date().isoformat(),
#         "Markaziy bankning dollar kursi": exchange_rates["usd"],
#         "Tanlangan valyuta": convert_to.upper(),
#         "Mahsulot ma'lumotlari": converted_expenses
#     }
#
#     return result