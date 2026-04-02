from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
from .. import schemas, crud
from ..database import get_db

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/", response_model=List[schemas.Product])
@limiter.limit("100/minute")
def get_products(
    request: Request,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in product name and description"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    color: Optional[str] = Query(None, description="Filter by color"),
    sort_by: Optional[str] = Query("created_at", description="Sort by field"),
    sort_order: Optional[str] = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """
    Get products with advanced filtering and sorting options
    """
    products = crud.get_products(
        db, 
        skip=skip, 
        limit=limit, 
        category=category,
        search=search,
        min_price=min_price,
        max_price=max_price,
        color=color,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return products

@router.get("/{product_id}", response_model=schemas.Product)
@limiter.limit("200/minute")
def get_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    """
    Get a specific product by ID
    """
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/categories/list", response_model=List[str])
@limiter.limit("50/minute")
def get_categories(request: Request, db: Session = Depends(get_db)):
    """
    Get all unique product categories
    """
    categories = crud.get_categories(db)
    return categories

@router.get("/colors/list", response_model=List[str])
@limiter.limit("50/minute")
def get_colors(request: Request, db: Session = Depends(get_db)):
    """
    Get all unique product colors
    """
    colors = crud.get_colors(db)
    return colors