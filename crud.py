from sqlalchemy.orm import Session

from models import BoardingSlot
from schemas import BoardingSlotCreate, BoardingSlotUpdate


def create_boarding_slot(db: Session, item: BoardingSlotCreate) -> BoardingSlot:
    try:
        db_item = BoardingSlot(
            slot_number=item.slot_number,
            room_size=item.room_size,
            price_per_day=item.price_per_day,
            status=item.status,
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception:
        db.rollback()
        raise


def get_boarding_slots(db: Session):
    try:
        return db.query(BoardingSlot).all()
    except Exception:
        db.rollback()
        raise


def get_boarding_slot(db: Session, slot_id: int):
    try:
        return db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
    except Exception:
        db.rollback()
        raise


def update_boarding_slot(db: Session, slot_id: int, item: BoardingSlotUpdate):
    try:
        db_item = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
        if not db_item:
            return None

        update_data = item.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception:
        db.rollback()
        raise


def delete_boarding_slot(db: Session, slot_id: int) -> bool:
    try:
        db_item = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
        if not db_item:
            return False

        db.delete(db_item)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
