"""
Game Catalog Service CRUD Operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func
from typing import Optional, List, Tuple
from . import models, schemas
import math

class GameCRUD:
    def __init__(self, db: Session):
        self.db = db
    
    def create_game(self, game: schemas.GameCreate) -> models.Game:
        """Create a new game"""
        db_game = models.Game(
            steam_app_id=game.steam_app_id,
            title=game.title,
            description=game.description,
            short_description=game.short_description,
            developer=game.developer,
            publisher=game.publisher,
            price=game.price,
            original_price=game.original_price,
            currency=game.currency,
            game_type=game.game_type.value,
            status=game.status.value,
            age_rating=game.age_rating.value if game.age_rating else None,
            release_date=game.release_date,
            early_access=game.early_access,
            single_player=game.single_player,
            multiplayer=game.multiplayer,
            co_op=game.co_op,
            local_co_op=game.local_co_op,
            cross_platform=game.cross_platform,
            vr_support=game.vr_support,
            header_image_url=game.header_image_url,
            background_image_url=game.background_image_url,
            capsule_image_url=game.capsule_image_url,
            screenshots=game.screenshots,
            movies=game.movies,
            pc_requirements=game.pc_requirements.dict() if game.pc_requirements else None,
            mac_requirements=game.mac_requirements.dict() if game.mac_requirements else None,
            linux_requirements=game.linux_requirements.dict() if game.linux_requirements else None,
        )
        
        # Calculate discount if original price is provided
        if game.original_price and game.original_price > game.price:
            db_game.discount_percent = round(((game.original_price - game.price) / game.original_price) * 100, 2)
        
        self.db.add(db_game)
        self.db.commit()
        self.db.refresh(db_game)
        
        # Add relationships
        if game.genre_ids:
            genres = self.db.query(models.Genre).filter(models.Genre.id.in_(game.genre_ids)).all()
            db_game.genres.extend(genres)
        
        if game.tag_ids:
            tags = self.db.query(models.Tag).filter(models.Tag.id.in_(game.tag_ids)).all()
            db_game.tags.extend(tags)
        
        if game.platform_ids:
            platforms = self.db.query(models.Platform).filter(models.Platform.id.in_(game.platform_ids)).all()
            db_game.platforms.extend(platforms)
        
        self.db.commit()
        return db_game
    
    def get_game_by_id(self, game_id: int) -> Optional[models.Game]:
        """Get game by ID"""
        return self.db.query(models.Game).filter(models.Game.id == game_id).first()
    
    def get_game_by_uuid(self, game_uuid: str) -> Optional[models.Game]:
        """Get game by UUID"""
        return self.db.query(models.Game).filter(models.Game.uuid == game_uuid).first()
    
    def get_game_by_steam_app_id(self, steam_app_id: int) -> Optional[models.Game]:
        """Get game by Steam App ID"""
        return self.db.query(models.Game).filter(models.Game.steam_app_id == steam_app_id).first()
    
    def update_game(self, game_id: int, game_update: schemas.GameUpdate) -> Optional[models.Game]:
        """Update game information"""
        db_game = self.get_game_by_id(game_id)
        if not db_game:
            return None
        
        update_data = game_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field in ['pc_requirements', 'mac_requirements', 'linux_requirements'] and value:
                setattr(db_game, field, value.dict())
            elif field in ['game_type', 'status', 'age_rating'] and value:
                setattr(db_game, field, value.value)
            else:
                setattr(db_game, field, value)
        
        # Recalculate discount if price changed
        if 'price' in update_data or 'original_price' in update_data:
            if db_game.original_price and db_game.original_price > db_game.price:
                db_game.discount_percent = round(((db_game.original_price - db_game.price) / db_game.original_price) * 100, 2)
            else:
                db_game.discount_percent = 0.0
        
        self.db.commit()
        self.db.refresh(db_game)
        return db_game
    
    def delete_game(self, game_id: int) -> bool:
        """Delete a game"""
        db_game = self.get_game_by_id(game_id)
        if not db_game:
            return False
        
        self.db.delete(db_game)
        self.db.commit()
        return True
    
    def search_games(self, filters: schemas.GameSearchFilters, page: int = 1, per_page: int = 20) -> Tuple[List[models.Game], int]:
        """Search games with filters and pagination"""
        query = self.db.query(models.Game)
        
        # Apply filters
        if filters.query:
            search_term = f"%{filters.query}%"
            query = query.filter(
                or_(
                    models.Game.title.ilike(search_term),
                    models.Game.description.ilike(search_term),
                    models.Game.developer.ilike(search_term),
                    models.Game.publisher.ilike(search_term)
                )
            )
        
        if filters.genres:
            query = query.join(models.Game.genres).filter(models.Genre.id.in_(filters.genres))
        
        if filters.tags:
            query = query.join(models.Game.tags).filter(models.Tag.id.in_(filters.tags))
        
        if filters.platforms:
            query = query.join(models.Game.platforms).filter(models.Platform.id.in_(filters.platforms))
        
        if filters.min_price is not None:
            query = query.filter(models.Game.price >= filters.min_price)
        
        if filters.max_price is not None:
            query = query.filter(models.Game.price <= filters.max_price)
        
        if filters.min_rating is not None:
            query = query.filter(models.Game.average_rating >= filters.min_rating)
        
        if filters.max_rating is not None:
            query = query.filter(models.Game.average_rating <= filters.max_rating)
        
        if filters.single_player is not None:
            query = query.filter(models.Game.single_player == filters.single_player)
        
        if filters.multiplayer is not None:
            query = query.filter(models.Game.multiplayer == filters.multiplayer)
        
        if filters.co_op is not None:
            query = query.filter(models.Game.co_op == filters.co_op)
        
        if filters.vr_support is not None:
            query = query.filter(models.Game.vr_support == filters.vr_support)
        
        if filters.early_access is not None:
            query = query.filter(models.Game.early_access == filters.early_access)
        
        if filters.status:
            query = query.filter(models.Game.status == filters.status.value)
        
        if filters.game_type:
            query = query.filter(models.Game.game_type == filters.game_type.value)
        
        if filters.age_rating:
            query = query.filter(models.Game.age_rating == filters.age_rating.value)
        
        # Apply sorting
        if filters.sort_by == "price":
            order_func = asc if filters.sort_order == "asc" else desc
            query = query.order_by(order_func(models.Game.price))
        elif filters.sort_by == "rating":
            order_func = asc if filters.sort_order == "asc" else desc
            query = query.order_by(order_func(models.Game.average_rating))
        elif filters.sort_by == "release_date":
            order_func = asc if filters.sort_order == "asc" else desc
            query = query.order_by(order_func(models.Game.release_date))
        elif filters.sort_by == "title":
            order_func = asc if filters.sort_order == "asc" else desc
            query = query.order_by(order_func(models.Game.title))
        else:  # relevance
            query = query.order_by(desc(models.Game.average_rating), desc(models.Game.total_reviews))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * per_page
        games = query.offset(offset).limit(per_page).all()
        
        return games, total
    
    def get_games(self, skip: int = 0, limit: int = 100) -> List[models.Game]:
        """Get list of games with pagination"""
        return self.db.query(models.Game).offset(skip).limit(limit).all()
    
    def get_featured_games(self, limit: int = 10) -> List[models.Game]:
        """Get featured games (highly rated, popular)"""
        return self.db.query(models.Game).filter(
            and_(
                models.Game.status == "active",
                models.Game.average_rating >= 4.0,
                models.Game.total_reviews >= 100
            )
        ).order_by(desc(models.Game.average_rating)).limit(limit).all()
    
    def get_new_releases(self, limit: int = 10) -> List[models.Game]:
        """Get new releases"""
        return self.db.query(models.Game).filter(
            and_(
                models.Game.status == "active",
                models.Game.release_date.isnot(None)
            )
        ).order_by(desc(models.Game.release_date)).limit(limit).all()
    
    def get_on_sale_games(self, limit: int = 10) -> List[models.Game]:
        """Get games on sale"""
        return self.db.query(models.Game).filter(
            and_(
                models.Game.status == "active",
                models.Game.discount_percent > 0
            )
        ).order_by(desc(models.Game.discount_percent)).limit(limit).all()

class GenreCRUD:
    def __init__(self, db: Session):
        self.db = db
    
    def create_genre(self, genre: schemas.GenreCreate) -> models.Genre:
        """Create a new genre"""
        db_genre = models.Genre(
            name=genre.name,
            description=genre.description
        )
        self.db.add(db_genre)
        self.db.commit()
        self.db.refresh(db_genre)
        return db_genre
    
    def get_genre_by_id(self, genre_id: int) -> Optional[models.Genre]:
        """Get genre by ID"""
        return self.db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    
    def get_genre_by_name(self, name: str) -> Optional[models.Genre]:
        """Get genre by name"""
        return self.db.query(models.Genre).filter(models.Genre.name == name).first()
    
    def get_genres(self, skip: int = 0, limit: int = 100) -> List[models.Genre]:
        """Get list of genres"""
        return self.db.query(models.Genre).offset(skip).limit(limit).all()

class TagCRUD:
    def __init__(self, db: Session):
        self.db = db
    
    def create_tag(self, tag: schemas.TagCreate) -> models.Tag:
        """Create a new tag"""
        db_tag = models.Tag(
            name=tag.name,
            description=tag.description,
            category=tag.category
        )
        self.db.add(db_tag)
        self.db.commit()
        self.db.refresh(db_tag)
        return db_tag
    
    def get_tag_by_id(self, tag_id: int) -> Optional[models.Tag]:
        """Get tag by ID"""
        return self.db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    
    def get_tag_by_name(self, name: str) -> Optional[models.Tag]:
        """Get tag by name"""
        return self.db.query(models.Tag).filter(models.Tag.name == name).first()
    
    def get_tags(self, skip: int = 0, limit: int = 100) -> List[models.Tag]:
        """Get list of tags"""
        return self.db.query(models.Tag).offset(skip).limit(limit).all()

class PlatformCRUD:
    def __init__(self, db: Session):
        self.db = db
    
    def create_platform(self, platform: schemas.PlatformCreate) -> models.Platform:
        """Create a new platform"""
        db_platform = models.Platform(
            name=platform.name,
            display_name=platform.display_name,
            description=platform.description,
            icon_url=platform.icon_url
        )
        self.db.add(db_platform)
        self.db.commit()
        self.db.refresh(db_platform)
        return db_platform
    
    def get_platform_by_id(self, platform_id: int) -> Optional[models.Platform]:
        """Get platform by ID"""
        return self.db.query(models.Platform).filter(models.Platform.id == platform_id).first()
    
    def get_platform_by_name(self, name: str) -> Optional[models.Platform]:
        """Get platform by name"""
        return self.db.query(models.Platform).filter(models.Platform.name == name).first()
    
    def get_platforms(self, skip: int = 0, limit: int = 100) -> List[models.Platform]:
        """Get list of platforms"""
        return self.db.query(models.Platform).offset(skip).limit(limit).all()