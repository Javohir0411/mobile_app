from fastapi import APIRouter
from fastapi import Depends
from app.db.crud import sell_item
from app.db.schemas import SellItemSchema
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.put("/sell/{item_id}")
def selling_item(item_id: int, sell_data: SellItemSchema, db: Session = Depends(get_db)):
    return sell_item(item_id, sell_data, db)
