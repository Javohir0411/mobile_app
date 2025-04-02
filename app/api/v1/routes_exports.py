from app.services.export_service import items_to_excel
from fastapi import APIRouter, Depends, Response, HTTPException, Query
from http.client import HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from typing import Optional
from app.services.export_service import income_to_excel, expense_to_excel, generate_pdf_income_report, \
    generate_expense_pdf_report
from app.services.report_service import get_income_report, get_expense_report
from fastapi.responses import FileResponse
import os
from app.core.security import get_current_user, verify_token

export_router = APIRouter()


# ----------- Bazadagi barcha mahsulotni excelga joylash uchun router ---------------

@export_router.get("/export/item-to-excel")
def save_to_excel(token: str = Query(..., description="Foydalanuvchi tokeni"), db: Session = Depends(get_db)):
    return items_to_excel(token, db)


# -----------------------------------------------------------


# ----------- Chiqim haqidagi ma'lumotlarni excelga joylash uchun router ---------------

@export_router.get("/export/expense-to-excel")
def save_expense_report_to_excel(token: str = Query(..., description="Foydalanuvchi tokeni"),
                                 period: Optional[str] = None,
                                 start_date: Optional[str] = None,
                                 end_date: Optional[str] = None,
                                 rate: Optional[float] = None,
                                 convert_to: str = "uzs",
                                 db: Session = Depends(get_db)):
    return expense_to_excel(token, db, period, start_date, end_date, rate, convert_to)

# -----------------------------------------------------------


# ----------- Tushum haqidagi ma'lumotlarni excelga joylash uchun router ---------------

@export_router.get("/export/income-to-excel")
def save_income_report_to_excel(db: Session = Depends(get_db),
                                token: str = Query(..., description="Foydalanuvchi tokeni"),
                                period: Optional[str] = None,
                                start_date: Optional[str] = None,
                                end_date: Optional[str] = None,
                                rate: Optional[float] = None,
                                convert_to: str = "uzs",):
    return income_to_excel(token, db, period, start_date, end_date, rate, convert_to)


# -----------------------------------------------------------


# - - - - - - PDF faylga saqlash - - - - - - - - - -

@export_router.get("/export/income/pdf")
def download_income_report(db: Session = Depends(get_db),
                           token: str = Query(..., description="Foydalanuvchi tokeni"),
                           period: Optional[str] = None,
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None,
                           rate: Optional[float] = None,
                           convert_to: str = "uzs"):

    user = verify_token(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Noto'gri token yoki user ro'yxatdan o'tmagan !")

    result = get_income_report(db, period, start_date, end_date, rate, convert_to)
    if "error" in result:
        return {"error": result["error"]}

    pdf_filename = "income_report.pdf"
    generate_pdf_income_report(db, result, pdf_filename, token)
    print(f"PDF fayl yaratildi: {pdf_filename}")

    if not os.path.exists(pdf_filename):
        return {"error": "PDF fayl yaratilmagan!"}

    return FileResponse(pdf_filename, media_type="application/pdf", filename=pdf_filename)


@export_router.get("/export/expense/pdf")
def download_expense_report(db: Session = Depends(get_db),
                            token: str = Query(..., description="Foydalanuvchi tokeni"),
                            period: Optional[str] = None,
                            start_date: Optional[str] = None,
                            end_date: Optional[str] = None,
                            rate: Optional[float] = None,
                            convert_to: str = "uzs"):
    user = verify_token(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Noto'g'ri token yoki user ro'yxatdan o'tmagan !")

    result = get_expense_report(db, period, start_date, end_date, rate, convert_to)
    # print(result)
    if "error" in result:
        return {"error": result["error"]}

    pdf_filename = "expense_report.pdf"
    generate_expense_pdf_report(db, result, pdf_filename, token)
    print(f"PDF yaratildi: {pdf_filename}")

    return FileResponse(pdf_filename, media_type="application/pdf", filename=pdf_filename)
