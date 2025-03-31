from app.services.export_service import items_to_excel
from fastapi import APIRouter, Depends, Response
from http.client import HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from typing import Optional
from app.services.export_service import income_to_excel, expense_to_excel, generate_pdf_income_report, \
    generate_expense_pdf_report
from app.services.report_service import get_income_report, get_expense_report
from fastapi.responses import FileResponse
import os
from app.core.security import get_current_user
export_router = APIRouter()


# ----------- Bazadagi barcha mahsulotni excelga joylash uchun router ---------------

@export_router.get("/export/item-to-excel")
def save_to_excel(db: Session = Depends(get_db)):
    return items_to_excel(db)


# -----------------------------------------------------------


# ----------- Chiqim haqidagi ma'lumotlarni excelga joylash uchun router ---------------

@export_router.get("/export/expense-to-excel")
def save_expense_report_to_excel(period: Optional[str] = None,
                                 start_date: Optional[str] = None,
                                 end_date: Optional[str] = None,
                                 rate: Optional[float] = None,
                                 convert_to: str = "uzs",
                                 db: Session = Depends(get_db)):
    return expense_to_excel(db, period, start_date, end_date, rate, convert_to)

# -----------------------------------------------------------


# ----------- Tushum haqidagi ma'lumotlarni excelga joylash uchun router ---------------

@export_router.get("/export/income-to-excel")
def save_income_report_to_excel(db: Session = Depends(get_db), period: Optional[str] = None, start_date: Optional[str] = None,
                    end_date: Optional[str] = None, rate: Optional[float] = None, convert_to: str = "uzs"):
    return income_to_excel(db, period, start_date, end_date, rate, convert_to)


# -----------------------------------------------------------


# - - - - - - PDF faylga saqlash - - - - - - - - - -

@export_router.get("/export/income/pdf")
def download_income_report(db: Session = Depends(get_db), period: Optional[str] = None, start_date: Optional[str] = None,
                    end_date: Optional[str] = None, rate: Optional[float] = None, convert_to: str = "uzs"):
    result = get_income_report(db, period, start_date, end_date, rate, convert_to)
    if "error" in result:
        return {"error": result["error"]}

    pdf_filename = "income_report.pdf"
    generate_pdf_income_report(result, pdf_filename)
    if not os.path.exists(pdf_filename):
        return {"error": "PDF fayl yaratilmagan!"}

    return FileResponse(pdf_filename, media_type="application/pdf", filename=pdf_filename)


@export_router.get("/export/expense/pdf")
def download_expense_report(db: Session = Depends(get_db), period: Optional[str] = None, start_date: Optional[str] = None,
                    end_date: Optional[str] = None, rate: Optional[float] = None, convert_to: str = "uzs"):
    result = get_expense_report(db, period, start_date, end_date, rate, convert_to)
    # print(result)
    if "error" in result:
        return {"error": result["error"]}

    pdf_filename = "expense_report.pdf"
    generate_expense_pdf_report(result, pdf_filename)
    print(f"PDF yaratildi: {pdf_filename}")

    return FileResponse(pdf_filename, media_type="application/pdf", filename=pdf_filename)


# ----------------- Ro'yxatdan o'tganlar uchun hisobot yuklash (Hozircha kerak emas) ---------------------

# @export_router.get("/report/pdf", response_class=Response)
# def download_pdf_report(user: dict = Depends(get_current_user)):
#     pdf_data = generate_pdf_report()  # PDF yaratish
#     headers = {
#         "Content-Disposition": "attachment; filename=hisobot.pdf",
#         "Content-Type": "application/pdf"
#     }
#     return Response(content=pdf_data, headers=headers)
#
# @export_router.get("/report/excel", response_class=Response)
# def download_excel_report(user: dict = Depends(get_current_user)):
#     excel_data = generate_excel_report()  # Excel yaratish
#     headers = {
#         "Content-Disposition": "attachment; filename=hisobot.xlsx",
#         "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     }
#     return Response(content=excel_data, headers=headers)