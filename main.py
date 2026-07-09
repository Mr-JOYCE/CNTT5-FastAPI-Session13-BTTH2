from datetime import datetime

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import crud
from database import Base, engine, get_db
from models import BoardingSlot
from schemas import APIResponse, BoardingSlotCreate, BoardingSlotRead, BoardingSlotUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Quản lý Boarding Slots",
    description="API CRUD cho hệ thống đặt chỗ dịch vụ chăm sóc thú cưng",
    version="1.0.0"
)


def get_timestamp() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def create_response(
    status_code: int,
    message: str,
    data=None,
    error: str = None,
    path: str = "/"
):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": get_timestamp(),
    }


def response_json(status_code: int, message: str, path: str, data=None, error: str = None):
    return JSONResponse(
        status_code=status_code,
        content=create_response(
            status_code=status_code,
            message=message,
            data=data,
            error=error,
            path=path,
        ),
    )


@app.post("/boarding-slots", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def create_boarding_slot(
    item: BoardingSlotCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    existing = db.query(BoardingSlot).filter(BoardingSlot.slot_number == item.slot_number).first()
    if existing:
        return response_json(
            status.HTTP_400_BAD_REQUEST,
            "Slot number already exists",
            str(request.url.path),
            data=None,
            error="Bad Request",
        )

    try:
        db_item = crud.create_boarding_slot(db, item)
        return response_json(
            status.HTTP_201_CREATED,
            "Tạo khoang lưu trú thành công",
            str(request.url.path),
            data={
                "id": db_item.id,
                "slot_number": db_item.slot_number,
                "room_size": db_item.room_size,
                "price_per_day": db_item.price_per_day,
                "status": db_item.status,
            },
        )
    except IntegrityError:
        return response_json(
            status.HTTP_400_BAD_REQUEST,
            "Slot number already exists",
            str(request.url.path),
            data=None,
            error="Bad Request",
        )
    except Exception:
        return response_json(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Lỗi hệ thống khi tạo khoang lưu trú",
            str(request.url.path),
            data=None,
            error="Internal Server Error",
        )


@app.get("/boarding-slots", response_model=APIResponse)
async def get_boarding_slots(request: Request, db: Session = Depends(get_db)):
    try:
        items = crud.get_boarding_slots(db)
        result = [
            {
                "id": item.id,
                "slot_number": item.slot_number,
                "room_size": item.room_size,
                "price_per_day": item.price_per_day,
                "status": item.status,
            }
            for item in items
        ]
        return response_json(
            status.HTTP_200_OK,
            "Lấy danh sách thành công",
            str(request.url.path),
            data=result,
        )
    except Exception:
        return response_json(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Lỗi hệ thống khi lấy danh sách",
            str(request.url.path),
            data=None,
            error="Internal Server Error",
        )


@app.get("/boarding-slots/{slot_id}", response_model=APIResponse)
async def get_boarding_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        db_item = crud.get_boarding_slot(db, slot_id)
        if not db_item:
            return response_json(
                status.HTTP_404_NOT_FOUND,
                "Không tìm thấy khoang lưu trú",
                str(request.url.path),
                data=None,
                error="Not Found",
            )
        return response_json(
            status.HTTP_200_OK,
            "Lấy thông tin khoang lưu trú thành công",
            str(request.url.path),
            data={
                "id": db_item.id,
                "slot_number": db_item.slot_number,
                "room_size": db_item.room_size,
                "price_per_day": db_item.price_per_day,
                "status": db_item.status,
            },
        )
    except Exception:
        return response_json(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Lỗi hệ thống khi lấy thông tin khoang lưu trú",
            str(request.url.path),
            data=None,
            error="Internal Server Error",
        )


@app.put("/boarding-slots/{slot_id}", response_model=APIResponse)
async def update_boarding_slot(
    slot_id: int,
    item: BoardingSlotUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    db_item = crud.get_boarding_slot(db, slot_id)
    if not db_item:
        return response_json(
            status.HTTP_404_NOT_FOUND,
            "Không tìm thấy khoang lưu trú",
            str(request.url.path),
            data=None,
            error="Not Found",
        )

    if item.slot_number and item.slot_number != db_item.slot_number:
        existing = db.query(BoardingSlot).filter(BoardingSlot.slot_number == item.slot_number).first()
        if existing:
            return response_json(
                status.HTTP_400_BAD_REQUEST,
                "Slot number already exists",
                str(request.url.path),
                data=None,
                error="Bad Request",
            )

    try:
        updated_item = crud.update_boarding_slot(db, slot_id, item)
        return response_json(
            status.HTTP_200_OK,
            "Cập nhật khoang lưu trú thành công",
            str(request.url.path),
            data={
                "id": updated_item.id,
                "slot_number": updated_item.slot_number,
                "room_size": updated_item.room_size,
                "price_per_day": updated_item.price_per_day,
                "status": updated_item.status,
            },
        )
    except IntegrityError:
        return response_json(
            status.HTTP_400_BAD_REQUEST,
            "Slot number already exists",
            str(request.url.path),
            data=None,
            error="Bad Request",
        )
    except Exception:
        return response_json(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Lỗi hệ thống khi cập nhật khoang lưu trú",
            str(request.url.path),
            data=None,
            error="Internal Server Error",
        )


@app.delete("/boarding-slots/{slot_id}", response_model=APIResponse)
async def delete_boarding_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        deleted = crud.delete_boarding_slot(db, slot_id)
        if not deleted:
            return response_json(
                status.HTTP_404_NOT_FOUND,
                "Không tìm thấy khoang lưu trú",
                str(request.url.path),
                data=None,
                error="Not Found",
            )
        return response_json(
            status.HTTP_200_OK,
            "Xóa khoang lưu trú thành công",
            str(request.url.path),
            data=None,
        )
    except Exception:
        return response_json(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Lỗi hệ thống khi xóa khoang lưu trú",
            str(request.url.path),
            data=None,
            error="Internal Server Error",
        )
