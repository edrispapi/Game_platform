"""CRUD helpers for the simplified catalog service."""
from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas


class GameCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_game(self, payload: schemas.GameCreate) -> models.Game:
        game = models.Game(
            title=payload.title,
            description=payload.description,
            price=payload.price,
            genre=payload.genre,
            platform=payload.platform,
        )
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        return game

    def get_game(self, game_id: int) -> Optional[models.Game]:
        return self.db.query(models.Game).filter(lambda g: g.id == game_id).first()

    def search_games(self, query: str) -> List[models.Game]:
        lowered = (query or "").lower()
        return [
            game for game in self.db.query(models.Game).all()
            if lowered in game.title.lower() or lowered in (game.description or "").lower()
        ]


def create_game(db: Session, payload: schemas.GameCreate) -> models.Game:
    return GameCRUD(db).create_game(payload)


def get_game(db: Session, game_id: int) -> Optional[models.Game]:
    return GameCRUD(db).get_game(game_id)


def search_games(db: Session, query: str) -> List[models.Game]:
    return GameCRUD(db).search_games(query)
