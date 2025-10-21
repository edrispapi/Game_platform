"""
Shopping Service CRUD Operations
"""
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

def create_cart(db: Session, cart: schemas.ShoppingCartCreate) -> models.ShoppingCart:
    """Create a new shopping cart"""
    db_cart = models.ShoppingCart(user_id=cart.user_id)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def get_cart(db: Session, cart_id: str) -> Optional[models.ShoppingCart]:
    """Get cart by ID"""
    return db.query(models.ShoppingCart).filter(models.ShoppingCart.id == cart_id).first()

def get_user_cart(db: Session, user_id: str) -> Optional[models.ShoppingCart]:
    """Get user's active cart"""
    return db.query(models.ShoppingCart).filter(models.ShoppingCart.user_id == user_id).first()

def add_cart_item(db: Session, cart_id: str, item: schemas.CartItemCreate) -> models.CartItem:
    """Add item to cart"""
    # Check if item already exists in cart
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart_id,
        models.CartItem.game_id == item.game_id
    ).first()
    
    if existing_item:
        existing_item.quantity += item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    
    db_item = models.CartItem(
        cart_id=cart_id,
        game_id=item.game_id,
        game_name=item.game_name,
        price=item.price,
        quantity=item.quantity
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_cart_item(db: Session, item_id: str, item_update: schemas.CartItemUpdate) -> Optional[models.CartItem]:
    """Update cart item"""
    db_item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    if not db_item:
        return None
    
    for field, value in item_update.dict(exclude_unset=True).items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

def remove_cart_item(db: Session, item_id: str) -> bool:
    """Remove item from cart"""
    db_item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    if not db_item:
        return False
    
    db.delete(db_item)
    db.commit()
    return True

def clear_cart(db: Session, cart_id: str) -> bool:
    """Clear all items from cart"""
    db.query(models.CartItem).filter(models.CartItem.cart_id == cart_id).delete()
    db.commit()
    return True

def create_wishlist(db: Session, wishlist: schemas.WishlistCreate) -> models.Wishlist:
    """Create a new wishlist"""
    db_wishlist = models.Wishlist(user_id=wishlist.user_id, name=wishlist.name)
    db.add(db_wishlist)
    db.commit()
    db.refresh(db_wishlist)
    return db_wishlist

def get_wishlist(db: Session, wishlist_id: str) -> Optional[models.Wishlist]:
    """Get wishlist by ID"""
    return db.query(models.Wishlist).filter(models.Wishlist.id == wishlist_id).first()

def get_user_wishlists(db: Session, user_id: str) -> List[models.Wishlist]:
    """Get user's wishlists"""
    return db.query(models.Wishlist).filter(models.Wishlist.user_id == user_id).all()

def add_wishlist_item(db: Session, wishlist_id: str, item: schemas.WishlistItemCreate) -> models.WishlistItem:
    """Add item to wishlist"""
    # Check if item already exists in wishlist
    existing_item = db.query(models.WishlistItem).filter(
        models.WishlistItem.wishlist_id == wishlist_id,
        models.WishlistItem.game_id == item.game_id
    ).first()
    
    if existing_item:
        return existing_item
    
    db_item = models.WishlistItem(
        wishlist_id=wishlist_id,
        game_id=item.game_id,
        game_name=item.game_name,
        price=item.price
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def remove_wishlist_item(db: Session, item_id: str) -> bool:
    """Remove item from wishlist"""
    db_item = db.query(models.WishlistItem).filter(models.WishlistItem.id == item_id).first()
    if not db_item:
        return False
    
    db.delete(db_item)
    db.commit()
    return True