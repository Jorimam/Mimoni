from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import model_expenses
from ..schemas import schema_expenses

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get("/health")
def index():
    return {"Message": "Manage your finance"}


@router.get("/get_all", response_model=List[schema_expenses.ExpensesResponse])
def get_expenses(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
):
    return (
        db.query(model_expenses.Expenses)
        .order_by(model_expenses.Expenses.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/by_id/{expense_id}", response_model=schema_expenses.ExpensesResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.get(model_expenses.Expenses, expense_id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense {expense_id} not found",
        )
    return expense


@router.post(
    "/create",
    response_model=schema_expenses.ExpensesResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_expense(
    expense_in: schema_expenses.ExpenseCreate, db: Session = Depends(get_db)
):
    new_expense = model_expenses.Expenses(**expense_in.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.patch("/{expense_id}", response_model=schema_expenses.ExpensesResponse)
def update_expense(
    expense_id: int,
    expense_in: schema_expenses.ExpensesUpdate,
    db: Session = Depends(get_db),
):
    expense = db.get(model_expenses.Expenses, expense_id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense {expense_id} not found",
        )
    for field, value in expense_in.model_dump(exclude_unset=True).items():
        setattr(expense, field, value)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.get(model_expenses.Expenses, expense_id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense {expense_id} not found",
        )
    db.delete(expense)
    db.commit()