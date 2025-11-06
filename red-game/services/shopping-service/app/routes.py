"""
Shopping Service API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas, database

router = APIRouter()

# Cart endpoints
@router.post("/cart", response_model=schemas.ShoppingCartResponse, status_code=status.HTTP_201_CREATED)
def create_cart(
    cart: schemas.ShoppingCartCreate,
    db: Session = Depends(database.get_db)
):
    """Create a new shopping cart"""
    return crud.create_cart(db=db, cart=cart)

@router.get("/cart/{cart_id}", response_model=schemas.ShoppingCartResponse)
def get_cart(
    cart_id: str,
    db: Session = Depends(database.get_db)
):
    """Get cart by ID"""
    cart = crud.get_cart(db=db, cart_id=cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.get("/cart/user/{user_id}", response_model=schemas.ShoppingCartResponse)
def get_user_cart(
    user_id: str,
    db: Session = Depends(database.get_db)
):
    """Get user's active cart"""
    cart = crud.get_user_cart(db=db, user_id=user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.post("/cart/{cart_id}/items", response_model=schemas.CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_cart_item(
    cart_id: str,
    item: schemas.CartItemCreate,
    db: Session = Depends(database.get_db)
):
    """Add item to cart"""
    return crud.add_cart_item(db=db, cart_id=cart_id, item=item)

@router.patch("/cart/items/{item_id}", response_model=schemas.CartItemResponse)
def update_cart_item(
    item_id: str,
    item_update: schemas.CartItemUpdate,
    db: Session = Depends(database.get_db)
):
    """Update cart item"""
    item = crud.update_cart_item(db=db, item_id=item_id, item_update=item_update)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return item

@router.delete("/cart/items/{item_id}")
def remove_cart_item(
    item_id: str,
    db: Session = Depends(database.get_db)
):
    """Remove item from cart"""
    if not crud.remove_cart_item(db=db, item_id=item_id):
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Item removed from cart"}

@router.delete("/cart/{cart_id}/clear")
def clear_cart(
    cart_id: str,
    db: Session = Depends(database.get_db)
):
    """Clear all items from cart"""
    crud.clear_cart(db=db, cart_id=cart_id)
    return {"message": "Cart cleared"}

# Wishlist endpoints
@router.post("/wishlist", response_model=schemas.WishlistResponse, status_code=status.HTTP_201_CREATED)
def create_wishlist(
    wishlist: schemas.WishlistCreate,
    db: Session = Depends(database.get_db)
):
    """Create a new wishlist"""
    return crud.create_wishlist(db=db, wishlist=wishlist)

@router.get("/wishlist/{wishlist_id}", response_model=schemas.WishlistResponse)
def get_wishlist(
    wishlist_id: str,
    db: Session = Depends(database.get_db)
):
    """Get wishlist by ID"""
    wishlist = crud.get_wishlist(db=db, wishlist_id=wishlist_id)
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    return wishlist

@router.get("/wishlist/user/{user_id}", response_model=List[schemas.WishlistResponse])
def get_user_wishlists(
    user_id: str,
    db: Session = Depends(database.get_db)
):
    """Get user's wishlists"""
    return crud.get_user_wishlists(db=db, user_id=user_id)

@router.post("/wishlist/{wishlist_id}/items", response_model=schemas.WishlistItemResponse, status_code=status.HTTP_201_CREATED)
def add_wishlist_item(
    wishlist_id: str,
    item: schemas.WishlistItemCreate,
    db: Session = Depends(database.get_db)
):
    """Add item to wishlist"""
    return crud.add_wishlist_item(db=db, wishlist_id=wishlist_id, item=item)

@router.delete("/wishlist/items/{item_id}")
def remove_wishlist_item(
    item_id: str,
    db: Session = Depends(database.get_db)
):
    """Remove item from wishlist"""
    if not crud.remove_wishlist_item(db=db, item_id=item_id):
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    return {"message": "Item removed from wishlist"}