from app.db.session import get_db
from app.services.report_service import get_income_report, get_expense_report, get_stock_with_value, get_statistics
from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

report_router = APIRouter()

# ---------- Tushum haqidagi ma'lumotni olish uchun router ---------------

# @report_router.get("/report/income")
# def read_income_reports(period: Optional[str] = None, period_date: Optional[str] = None, rate: Optional[float] = None,
#                         convert_to: str = "uzs", db: Session = Depends(get_db)):
#     return get_income_report(db, period, period_date, rate, convert_to)

@report_router.get("/report/income")
def read_income_reports(period: Optional[str] = None,
                        start_date: Optional[str] = None,
                        end_date: Optional[str] = None,
                        rate: Optional[float] = None, convert_to: str = "uzs",
                        db: Session = Depends(get_db)):
    return get_income_report(db, period, start_date, end_date, rate, convert_to)

# -----------------------------------------------------------


# ----------- Chiqim haqidagi ma'lumotni olish uchun router ---------------

# @report_router.get("/report/expense")
# def read_expense_reports(period: Optional[str] = None, period_date: Optional[str] = None, rate: Optional[float] = None,
#                          convert_to: str = "uzs", db: Session = Depends(get_db)):
#     return get_expense_report(db, period, period_date, rate, convert_to)

@report_router.get("/report/expense")
def read_expense_reports(
    period: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    rate: Optional[float] = None,
    convert_to: str = "uzs",
    db: Session = Depends(get_db)
):
    return get_expense_report(db, period, start_date, end_date, rate, convert_to)

# -----------------------------------------------------------

# ----------- Omborxona haqidagi ma'lumotni olish uchun router ---------------

@report_router.get("/report/leftovers")
def read_remaining_with_value(db: Session = Depends(get_db)):
    return get_stock_with_value(db)

# -----------------------------------------------------------

# ----------- Statistika haqidagi ma'lumotni olish uchun router ---------------

@report_router.get("/report/statistics")
def read_statistics(
        period: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        rate: Optional[float] = None,
        convert_to: str = "uzs",
        lang: str = "uz",
        db: Session = Depends(get_db)):
    return get_statistics(db, period, start_date, end_date, rate, convert_to, lang)